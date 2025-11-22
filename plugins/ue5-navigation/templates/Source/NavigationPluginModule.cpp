// ==========================================
// UE5 Navigation Plugin - Module Implementation
// ==========================================

#include "NavigationPluginModule.h"
#include "NavigationServer.h"
#include "LevelEditor.h"
#include "ToolMenus.h"
#include "Widgets/Docking/SDockTab.h"
#include "WorkspaceMenuStructure.h"
#include "WorkspaceMenuStructureModule.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"

#define LOCTEXT_NAMESPACE "FNavigationPluginModule"

IMPLEMENT_MODULE(FNavigationPluginModule, NavigationPlugin)

void FNavigationPluginModule::StartupModule()
{
    UE_LOG(LogTemp, Log, TEXT("NavigationPlugin: Module started"));

    // Register menu extensions
    RegisterMenuExtensions();

    // Initialize the navigation server
    NavigationServer = NewObject<UNavigationServer>();
    if (NavigationServer)
    {
        NavigationServer->AddToRoot(); // Prevent garbage collection
        UE_LOG(LogTemp, Log, TEXT("NavigationPlugin: NavigationServer initialized"));
    }
}

void FNavigationPluginModule::ShutdownModule()
{
    UE_LOG(LogTemp, Log, TEXT("NavigationPlugin: Module shutting down"));

    // Cleanup menu extensions
    UnregisterMenuExtensions();

    // Stop the server if running
    if (NavigationServer && NavigationServer->IsServerRunning())
    {
        NavigationServer->StopHTTPServer();
    }

    // Remove from root to allow garbage collection
    if (NavigationServer)
    {
        NavigationServer->RemoveFromRoot();
        NavigationServer = nullptr;
    }
}

void FNavigationPluginModule::RegisterMenuExtensions()
{
    UToolMenus::RegisterStartupCallback(
        FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FNavigationPluginModule::RegisterMenus)
    );
}

void FNavigationPluginModule::UnregisterMenuExtensions()
{
    UToolMenus::UnRegisterStartupCallback(this);
    UToolMenus::UnregisterOwner(this);
}

void FNavigationPluginModule::RegisterMenus()
{
    FToolMenuOwnerScoped OwnerScoped(this);

    // Add to the Tools menu
    {
        UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Tools");
        if (Menu)
        {
            FToolMenuSection& Section = Menu->FindOrAddSection("NavigationTools");
            Section.AddMenuEntryWithCommandList(
                "StartNavigationServer",
                LOCTEXT("StartNavigationServer", "Start Navigation Server"),
                LOCTEXT("StartNavigationServerTooltip", "Start the HTTP Navigation Server on port 8080"),
                FSlateIcon(),
                FUIAction(FExecuteAction::CreateRaw(this, &FNavigationPluginModule::OnStartServer))
            );

            Section.AddMenuEntryWithCommandList(
                "StopNavigationServer",
                LOCTEXT("StopNavigationServer", "Stop Navigation Server"),
                LOCTEXT("StopNavigationServerTooltip", "Stop the HTTP Navigation Server"),
                FSlateIcon(),
                FUIAction(FExecuteAction::CreateRaw(this, &FNavigationPluginModule::OnStopServer))
            );
        }
    }

    // Add toolbar button
    {
        UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.User");
        if (ToolbarMenu)
        {
            FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("NavigationPlugin");
            Section.AddEntry(FToolMenuEntry::InitToolBarButton(
                "ToggleNavigationServer",
                FUIAction(
                    FExecuteAction::CreateRaw(this, &FNavigationPluginModule::OnToggleServer),
                    FCanExecuteAction(),
                    FIsActionChecked::CreateRaw(this, &FNavigationPluginModule::IsServerRunning)
                ),
                LOCTEXT("ToggleNavigationServer", "Navigation Server"),
                LOCTEXT("ToggleNavigationServerTooltip", "Toggle Navigation HTTP Server"),
                FSlateIcon()
            ));
        }
    }
}

void FNavigationPluginModule::OnStartServer()
{
    if (NavigationServer)
    {
        NavigationServer->StartHTTPServer(8080);
    }
}

void FNavigationPluginModule::OnStopServer()
{
    if (NavigationServer)
    {
        NavigationServer->StopHTTPServer();
    }
}

void FNavigationPluginModule::OnToggleServer()
{
    if (NavigationServer)
    {
        if (NavigationServer->IsServerRunning())
        {
            NavigationServer->StopHTTPServer();
        }
        else
        {
            NavigationServer->StartHTTPServer(8080);
        }
    }
}

bool FNavigationPluginModule::IsServerRunning() const
{
    return NavigationServer && NavigationServer->IsServerRunning();
}

UNavigationServer* FNavigationPluginModule::GetNavigationServer() const
{
    return NavigationServer;
}

#undef LOCTEXT_NAMESPACE
