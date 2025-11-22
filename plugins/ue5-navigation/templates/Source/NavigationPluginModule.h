// ==========================================
// UE5 Navigation Plugin - Module Header
// ==========================================

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class UNavigationServer;

class FNavigationPluginModule : public IModuleInterface
{
public:
    /** IModuleInterface implementation */
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

    /** Get the navigation server instance */
    UNavigationServer* GetNavigationServer() const;

private:
    /** Register menu extensions */
    void RegisterMenuExtensions();

    /** Unregister menu extensions */
    void UnregisterMenuExtensions();

    /** Register menus */
    void RegisterMenus();

    /** Menu callbacks */
    void OnStartServer();
    void OnStopServer();
    void OnToggleServer();

    /** Server state check */
    bool IsServerRunning() const;

private:
    /** Navigation server instance */
    UPROPERTY()
    UNavigationServer* NavigationServer = nullptr;
};
