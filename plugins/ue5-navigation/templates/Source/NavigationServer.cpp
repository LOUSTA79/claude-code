// ==========================================
// UE5 Navigation Plugin - NavigationServer.cpp
// ==========================================

#include "NavigationServer.h"
#include "HttpModule.h"
#include "HttpServerModule.h"
#include "IHttpRouter.h"
#include "HttpPath.h"
#include "HttpServerRequest.h"
#include "HttpServerResponse.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
#include "Dom/JsonObject.h"
#include "AssetRegistry/AssetData.h"
#include "EditorAssetLibrary.h"
#include "LevelEditor.h"
#include "IAssetViewport.h"
#include "EditorViewportClient.h"
#include "Subsystems/EditorActorSubsystem.h"
#include "Engine/Selection.h"
#include "FileHelpers.h"

UNavigationServer::UNavigationServer()
    : bServerRunning(false)
    , ServerPort(8080)
{
}

// ==========================================
// Server Management
// ==========================================

void UNavigationServer::StartHTTPServer(int32 Port)
{
    if (bServerRunning)
    {
        UE_LOG(LogTemp, Warning, TEXT("Navigation Server is already running on port %d"), ServerPort);
        ShowNotification(FString::Printf(TEXT("Server already running on port %d"), ServerPort), false);
        return;
    }

    ServerPort = Port;

    // Initialize HTTP Server Module
    HttpServerModule = MakeShared<FHttpServerModule>();
    HttpRouter = HttpServerModule->GetHttpRouter(ServerPort);

    if (!HttpRouter.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create HTTP Router"));
        ShowNotification(TEXT("Failed to start Navigation Server"), false);
        return;
    }

    // Register Routes
    FHttpRouteHandle RouteHandle = HttpRouter->BindRoute(
        FHttpPath(TEXT("/api/navigate")),
        EHttpServerRequestVerbs::VERB_POST,
        [this](const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
        {
            FString RequestBody = FString(Request.Body.Num(), UTF8_TO_TCHAR(Request.Body.GetData()));
            HandleHTTPRequest(RequestBody);

            // Create response
            TUniquePtr<FHttpServerResponse> Response = FHttpServerResponse::Create(TEXT("{\"status\":\"ok\"}"), TEXT("application/json"));
            OnComplete(MoveTemp(Response));
            return true;
        }
    );

    // Start the server
    HttpServerModule->StartAllListeners();
    bServerRunning = true;

    UE_LOG(LogTemp, Log, TEXT("Navigation Server started on port %d"), ServerPort);
    ShowNotification(FString::Printf(TEXT("Navigation Server started on port %d"), ServerPort), true);
}

void UNavigationServer::StopHTTPServer()
{
    if (!bServerRunning)
    {
        UE_LOG(LogTemp, Warning, TEXT("Navigation Server is not running"));
        return;
    }

    if (HttpServerModule.IsValid())
    {
        HttpServerModule->StopAllListeners();
    }

    HttpRouter.Reset();
    HttpServerModule.Reset();
    bServerRunning = false;

    UE_LOG(LogTemp, Log, TEXT("Navigation Server stopped"));
    ShowNotification(TEXT("Navigation Server stopped"), true);
}

bool UNavigationServer::IsServerRunning() const
{
    return bServerRunning;
}

// ==========================================
// Command Processing
// ==========================================

FNavigationResponse UNavigationServer::ProcessCommand(const FNavigationCommand& Command)
{
    FNavigationResponse Response;
    FString ValidationError;

    if (!ValidateCommand(Command, ValidationError))
    {
        Response.Success = false;
        Response.Error = ValidationError;
        return Response;
    }

    // Route command to appropriate handler
    if (Command.Command == TEXT("FocusAsset"))
    {
        Response = HandleFocusAssetCommand(Command);
    }
    else if (Command.Command == TEXT("OpenAsset"))
    {
        Response = HandleOpenAssetCommand(Command);
    }
    else if (Command.Command == TEXT("Search"))
    {
        Response = HandleSearchCommand(Command);
    }
    else if (Command.Command == TEXT("Navigate"))
    {
        Response = HandleNavigateCommand(Command);
    }
    else if (Command.Command == TEXT("Blueprint"))
    {
        Response = HandleBlueprintCommand(Command);
    }
    else
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Unknown command: %s"), *Command.Command);
    }

    return Response;
}

// ==========================================
// Asset Navigation
// ==========================================

FNavigationResponse UNavigationServer::FocusAsset(const FString& AssetName)
{
    FNavigationResponse Response;

    UObject* Asset = FindAssetByName(AssetName);
    if (!Asset)
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Asset not found: %s"), *AssetName);
        return Response;
    }

    // Focus in Content Browser
    TArray<UObject*> Assets;
    Assets.Add(Asset);

    FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
    ContentBrowserModule.Get().SyncBrowserToAssets(Assets);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Focused on asset: %s"), *AssetName);

    AddBreadcrumb(Asset->GetPathName(), FString::Printf(TEXT("Focused: %s"), *AssetName));
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::OpenAsset(const FString& AssetPath)
{
    FNavigationResponse Response;

    UObject* Asset = UEditorAssetLibrary::LoadAsset(AssetPath);
    if (!Asset)
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Failed to load asset: %s"), *AssetPath);
        return Response;
    }

    // Open the asset in the appropriate editor
    GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->OpenEditorForAsset(Asset);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Opened asset: %s"), *AssetPath);

    AddBreadcrumb(AssetPath, FString::Printf(TEXT("Opened: %s"), *AssetPath));
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::SearchAssets(const FString& SearchTerm)
{
    FNavigationResponse Response;

    FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
    IAssetRegistry& AssetRegistry = AssetRegistryModule.Get();

    TArray<FAssetData> AssetDataList;
    AssetRegistry.GetAllAssets(AssetDataList);

    TArray<FString> MatchingAssets;
    for (const FAssetData& AssetData : AssetDataList)
    {
        if (AssetData.AssetName.ToString().Contains(SearchTerm))
        {
            MatchingAssets.Add(AssetData.ObjectPath.ToString());
        }
    }

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Found %d assets matching '%s'"), MatchingAssets.Num(), *SearchTerm);

    for (int32 i = 0; i < FMath::Min(MatchingAssets.Num(), 10); i++)
    {
        Response.AdditionalData.Add(FString::Printf(TEXT("Result_%d"), i), MatchingAssets[i]);
    }

    return Response;
}

// ==========================================
// Editor Navigation
// ==========================================

FNavigationResponse UNavigationServer::NavigateToLocation(const FVector& Location)
{
    FNavigationResponse Response;

    FLevelEditorModule& LevelEditorModule = FModuleManager::GetModuleChecked<FLevelEditorModule>("LevelEditor");
    TSharedPtr<IAssetViewport> ActiveViewport = LevelEditorModule.GetFirstActiveViewport();

    if (!ActiveViewport.IsValid())
    {
        Response.Success = false;
        Response.Error = TEXT("No active viewport found");
        return Response;
    }

    FEditorViewportClient& ViewportClient = ActiveViewport->GetAssetViewportClient();
    ViewportClient.SetViewLocation(Location);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Navigated to location: %s"), *Location.ToString());

    AddBreadcrumb(TEXT("Viewport"), Response.Message);
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::OpenEditorWindow(const FString& WindowType)
{
    FNavigationResponse Response;

    if (WindowType == TEXT("ContentBrowser"))
    {
        FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
        ContentBrowserModule.Get().SyncBrowserToAssets(TArray<FAssetData>());
    }
    else if (WindowType == TEXT("OutputLog"))
    {
        FGlobalTabmanager::Get()->TryInvokeTab(FName("OutputLog"));
    }
    else if (WindowType == TEXT("Viewport"))
    {
        FGlobalTabmanager::Get()->TryInvokeTab(FName("LevelEditor"));
    }
    else
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Unknown window type: %s"), *WindowType);
        return Response;
    }

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Opened editor window: %s"), *WindowType);
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::SwitchLevel(const FString& LevelName)
{
    FNavigationResponse Response;

    FString LevelPath = FString::Printf(TEXT("/Game/Maps/%s"), *LevelName);
    bool bSuccess = UEditorAssetLibrary::DoesAssetExist(LevelPath);

    if (!bSuccess)
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Level not found: %s"), *LevelName);
        return Response;
    }

    FEditorFileUtils::LoadMap(LevelPath + TEXT(".") + LevelName);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Switched to level: %s"), *LevelName);

    AddBreadcrumb(LevelPath, FString::Printf(TEXT("Level: %s"), *LevelName));
    ShowNotification(Response.Message, true);

    return Response;
}

// ==========================================
// Blueprint Navigation
// ==========================================

FNavigationResponse UNavigationServer::FindBlueprintNode(const FString& BlueprintPath, const FString& NodeName)
{
    FNavigationResponse Response;

    UObject* Asset = UEditorAssetLibrary::LoadAsset(BlueprintPath);
    if (!Asset || !Asset->IsA<UBlueprint>())
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Invalid blueprint: %s"), *BlueprintPath);
        return Response;
    }

    // Open the blueprint
    GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->OpenEditorForAsset(Asset);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Opened blueprint, searching for node: %s"), *NodeName);
    Response.AdditionalData.Add(TEXT("BlueprintPath"), BlueprintPath);
    Response.AdditionalData.Add(TEXT("NodeName"), NodeName);

    return Response;
}

FNavigationResponse UNavigationServer::HighlightBlueprintNode(const FString& BlueprintPath, const FString& NodeID)
{
    FNavigationResponse Response;

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Highlighting node %s in %s"), *NodeID, *BlueprintPath);

    return Response;
}

// ==========================================
// Code Navigation
// ==========================================

FNavigationResponse UNavigationServer::OpenSourceFile(const FString& FilePath, int32 LineNumber)
{
    FNavigationResponse Response;

    if (!FPaths::FileExists(FilePath))
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("File not found: %s"), *FilePath);
        return Response;
    }

    // Open in IDE (Visual Studio, Rider, etc.)
    FSourceCodeNavigation::OpenSourceFile(FilePath, LineNumber);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Opened source file: %s:%d"), *FilePath, LineNumber);

    AddBreadcrumb(FilePath, FString::Printf(TEXT("Source: %s:%d"), *FPaths::GetCleanFilename(FilePath), LineNumber));
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::FindSymbol(const FString& SymbolName)
{
    FNavigationResponse Response;

    // This would integrate with IDE symbol search
    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Searching for symbol: %s"), *SymbolName);
    Response.AdditionalData.Add(TEXT("SymbolName"), SymbolName);

    return Response;
}

// ==========================================
// Viewport Control
// ==========================================

FNavigationResponse UNavigationServer::SetViewportCamera(const FVector& Location, const FRotator& Rotation)
{
    FNavigationResponse Response;

    FLevelEditorModule& LevelEditorModule = FModuleManager::GetModuleChecked<FLevelEditorModule>("LevelEditor");
    TSharedPtr<IAssetViewport> ActiveViewport = LevelEditorModule.GetFirstActiveViewport();

    if (!ActiveViewport.IsValid())
    {
        Response.Success = false;
        Response.Error = TEXT("No active viewport found");
        return Response;
    }

    FEditorViewportClient& ViewportClient = ActiveViewport->GetAssetViewportClient();
    ViewportClient.SetViewLocation(Location);
    ViewportClient.SetViewRotation(Rotation);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Set camera to location: %s, rotation: %s"), *Location.ToString(), *Rotation.ToString());

    return Response;
}

FNavigationResponse UNavigationServer::FocusOnActor(const FString& ActorName)
{
    FNavigationResponse Response;

    UEditorActorSubsystem* EditorActorSubsystem = GEditor->GetEditorSubsystem<UEditorActorSubsystem>();
    if (!EditorActorSubsystem)
    {
        Response.Success = false;
        Response.Error = TEXT("Failed to get EditorActorSubsystem");
        return Response;
    }

    TArray<AActor*> AllActors = EditorActorSubsystem->GetAllLevelActors();
    AActor* TargetActor = nullptr;

    for (AActor* Actor : AllActors)
    {
        if (Actor && Actor->GetName() == ActorName)
        {
            TargetActor = Actor;
            break;
        }
    }

    if (!TargetActor)
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Actor not found: %s"), *ActorName);
        return Response;
    }

    // Select and focus on actor
    GEditor->SelectNone(false, true);
    GEditor->SelectActor(TargetActor, true, true);
    GEditor->NoteSelectionChange();
    GEditor->MoveViewportCamerasToActor(*TargetActor, false);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Focused on actor: %s"), *ActorName);

    AddBreadcrumb(TEXT("Actor"), Response.Message);
    ShowNotification(Response.Message, true);

    return Response;
}

// ==========================================
// Project Structure
// ==========================================

FNavigationResponse UNavigationServer::GetProjectStructure()
{
    FNavigationResponse Response;

    FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
    IAssetRegistry& AssetRegistry = AssetRegistryModule.Get();

    TArray<FString> ContentPaths;
    AssetRegistry.GetAllCachedPaths(ContentPaths);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Found %d paths in project"), ContentPaths.Num());

    for (int32 i = 0; i < FMath::Min(ContentPaths.Num(), 50); i++)
    {
        Response.AdditionalData.Add(FString::Printf(TEXT("Path_%d"), i), ContentPaths[i]);
    }

    return Response;
}

FNavigationResponse UNavigationServer::GetAssetHierarchy(const FString& RootPath)
{
    FNavigationResponse Response;

    TArray<FString> Assets;
    UEditorAssetLibrary::ListAssets(RootPath, Assets, true);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Found %d assets in %s"), Assets.Num(), *RootPath);

    for (int32 i = 0; i < FMath::Min(Assets.Num(), 50); i++)
    {
        Response.AdditionalData.Add(FString::Printf(TEXT("Asset_%d"), i), Assets[i]);
    }

    return Response;
}

// ==========================================
// Session Management
// ==========================================

FNavigationResponse UNavigationServer::SaveNavigationSession(const FString& SessionName)
{
    FNavigationResponse Response;

    // Serialize current state
    FString SessionData;
    for (int32 i = 0; i < BreadcrumbHistory.Num(); i++)
    {
        SessionData += BreadcrumbHistory[i] + TEXT("\n");
    }

    SessionCache.Add(SessionName, SessionData);

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Saved navigation session: %s"), *SessionName);
    ShowNotification(Response.Message, true);

    return Response;
}

FNavigationResponse UNavigationServer::LoadNavigationSession(const FString& SessionName)
{
    FNavigationResponse Response;

    if (!SessionCache.Contains(SessionName))
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Session not found: %s"), *SessionName);
        return Response;
    }

    FString SessionData = SessionCache[SessionName];
    BreadcrumbHistory.Empty();
    SessionData.ParseIntoArray(BreadcrumbHistory, TEXT("\n"));

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Loaded navigation session: %s"), *SessionName);
    ShowNotification(Response.Message, true);

    return Response;
}

// ==========================================
// Breadcrumb System
// ==========================================

void UNavigationServer::AddBreadcrumb(const FString& Location, const FString& Description)
{
    FString Breadcrumb = FString::Printf(TEXT("[%s] %s: %s"),
        *FDateTime::Now().ToString(), *Location, *Description);
    BreadcrumbHistory.Add(Breadcrumb);

    // Keep history to last 100 items
    if (BreadcrumbHistory.Num() > 100)
    {
        BreadcrumbHistory.RemoveAt(0);
    }
}

TArray<FString> UNavigationServer::GetBreadcrumbHistory()
{
    return BreadcrumbHistory;
}

FNavigationResponse UNavigationServer::NavigateToBreadcrumb(int32 Index)
{
    FNavigationResponse Response;

    if (Index < 0 || Index >= BreadcrumbHistory.Num())
    {
        Response.Success = false;
        Response.Error = FString::Printf(TEXT("Invalid breadcrumb index: %d"), Index);
        return Response;
    }

    Response.Success = true;
    Response.Message = FString::Printf(TEXT("Navigating to breadcrumb: %s"), *BreadcrumbHistory[Index]);
    Response.AdditionalData.Add(TEXT("Breadcrumb"), BreadcrumbHistory[Index]);

    return Response;
}

// ==========================================
// HTTP Server Implementation
// ==========================================

void UNavigationServer::HandleHTTPRequest(const FString& RequestBody)
{
    FNavigationCommand Command = ParseJSONCommand(RequestBody);
    FNavigationResponse Response = ProcessCommand(Command);

    UE_LOG(LogTemp, Log, TEXT("Processed command: %s, Success: %s"), *Command.Command, Response.Success ? TEXT("true") : TEXT("false"));
}

FString UNavigationServer::CreateJSONResponse(const FNavigationResponse& Response)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShared<FJsonObject>();
    JsonObject->SetBoolField(TEXT("success"), Response.Success);
    JsonObject->SetStringField(TEXT("message"), Response.Message);
    JsonObject->SetStringField(TEXT("error"), Response.Error);
    JsonObject->SetNumberField(TEXT("progress"), Response.Progress);

    TSharedPtr<FJsonObject> AdditionalDataJson = MakeShared<FJsonObject>();
    for (const auto& Pair : Response.AdditionalData)
    {
        AdditionalDataJson->SetStringField(Pair.Key, Pair.Value);
    }
    JsonObject->SetObjectField(TEXT("additionalData"), AdditionalDataJson);

    FString OutputString;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    return OutputString;
}

FNavigationCommand UNavigationServer::ParseJSONCommand(const FString& JSONString)
{
    FNavigationCommand Command;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSONString);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        JsonObject->TryGetStringField(TEXT("command"), Command.Command);
        JsonObject->TryGetStringField(TEXT("assetName"), Command.AssetName);
        JsonObject->TryGetStringField(TEXT("editorType"), Command.EditorType);
        JsonObject->TryGetStringField(TEXT("timestamp"), Command.Timestamp);

        // Parse location if present
        const TSharedPtr<FJsonObject>* LocationObject;
        if (JsonObject->TryGetObjectField(TEXT("location"), LocationObject))
        {
            double X, Y, Z;
            (*LocationObject)->TryGetNumberField(TEXT("x"), X);
            (*LocationObject)->TryGetNumberField(TEXT("y"), Y);
            (*LocationObject)->TryGetNumberField(TEXT("z"), Z);
            Command.Location = FVector(X, Y, Z);
        }
    }

    return Command;
}

// ==========================================
// Command Handlers
// ==========================================

FNavigationResponse UNavigationServer::HandleFocusAssetCommand(const FNavigationCommand& Command)
{
    return FocusAsset(Command.AssetName);
}

FNavigationResponse UNavigationServer::HandleOpenAssetCommand(const FNavigationCommand& Command)
{
    return OpenAsset(Command.AssetName);
}

FNavigationResponse UNavigationServer::HandleSearchCommand(const FNavigationCommand& Command)
{
    return SearchAssets(Command.AssetName);
}

FNavigationResponse UNavigationServer::HandleNavigateCommand(const FNavigationCommand& Command)
{
    return NavigateToLocation(Command.Location);
}

FNavigationResponse UNavigationServer::HandleBlueprintCommand(const FNavigationCommand& Command)
{
    return FindBlueprintNode(Command.AssetName, Command.EditorType);
}

// ==========================================
// Helper Methods
// ==========================================

UObject* UNavigationServer::FindAssetByName(const FString& AssetName)
{
    FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
    IAssetRegistry& AssetRegistry = AssetRegistryModule.Get();

    TArray<FAssetData> AssetDataList;
    AssetRegistry.GetAssetsByClass(UObject::StaticClass()->GetFName(), AssetDataList);

    for (const FAssetData& AssetData : AssetDataList)
    {
        if (AssetData.AssetName.ToString() == AssetName)
        {
            return AssetData.GetAsset();
        }
    }

    return nullptr;
}

void UNavigationServer::ShowNotification(const FString& Message, bool bSuccess)
{
    FNotificationInfo Info(FText::FromString(Message));
    Info.ExpireDuration = 3.0f;
    Info.bUseSuccessFailIcons = true;
    Info.Image = bSuccess ?
        FCoreStyle::Get().GetBrush(TEXT("NotificationList.SuccessImage")) :
        FCoreStyle::Get().GetBrush(TEXT("NotificationList.FailImage"));

    FSlateNotificationManager::Get().AddNotification(Info);
}

bool UNavigationServer::ValidateCommand(const FNavigationCommand& Command, FString& OutError)
{
    if (Command.Command.IsEmpty())
    {
        OutError = TEXT("Command cannot be empty");
        return false;
    }

    return true;
}
