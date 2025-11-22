// ==========================================
// UE5 Navigation Plugin - NavigationServer.h
// ==========================================

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Engine/Engine.h"
#include "Editor/EditorEngine.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "ContentBrowserModule.h"
#include "ToolMenus.h"
#include "Framework/Notifications/NotificationManager.h"
#include "Widgets/Notifications/SNotificationList.h"
#include "NavigationServer.generated.h"

USTRUCT(BlueprintType)
struct FNavigationCommand
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString Command;

    UPROPERTY(BlueprintReadWrite)
    FString AssetName;

    UPROPERTY(BlueprintReadWrite)
    FVector Location;

    UPROPERTY(BlueprintReadWrite)
    FString EditorType;

    UPROPERTY(BlueprintReadWrite)
    FString Timestamp;
};

USTRUCT(BlueprintType)
struct FNavigationResponse
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    bool Success = false;

    UPROPERTY(BlueprintReadWrite)
    FString Message;

    UPROPERTY(BlueprintReadWrite)
    FString Error;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, FString> AdditionalData;

    UPROPERTY(BlueprintReadWrite)
    float Progress = 0.0f;
};

UCLASS(BlueprintType, Blueprintable)
class NAVIGATIONPLUGIN_API UNavigationServer : public UObject
{
    GENERATED_BODY()

public:
    UNavigationServer();

    // Server Management
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    void StartHTTPServer(int32 Port = 8080);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    void StopHTTPServer();

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    bool IsServerRunning() const;

    // Command Processing
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse ProcessCommand(const FNavigationCommand& Command);

    // Asset Navigation
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse FocusAsset(const FString& AssetName);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse OpenAsset(const FString& AssetPath);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse SearchAssets(const FString& SearchTerm);

    // Editor Navigation
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse NavigateToLocation(const FVector& Location);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse OpenEditorWindow(const FString& WindowType);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse SwitchLevel(const FString& LevelName);

    // Blueprint Navigation
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse FindBlueprintNode(const FString& BlueprintPath, const FString& NodeName);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse HighlightBlueprintNode(const FString& BlueprintPath, const FString& NodeID);

    // Code Navigation
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse OpenSourceFile(const FString& FilePath, int32 LineNumber = -1);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse FindSymbol(const FString& SymbolName);

    // Viewport Control
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse SetViewportCamera(const FVector& Location, const FRotator& Rotation);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse FocusOnActor(const FString& ActorName);

    // Project Structure
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse GetProjectStructure();

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse GetAssetHierarchy(const FString& RootPath);

    // Session Management
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse SaveNavigationSession(const FString& SessionName);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse LoadNavigationSession(const FString& SessionName);

    // Breadcrumb System
    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    void AddBreadcrumb(const FString& Location, const FString& Description);

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    TArray<FString> GetBreadcrumbHistory();

    UFUNCTION(BlueprintCallable, Category = "Navigation Server")
    FNavigationResponse NavigateToBreadcrumb(int32 Index);

protected:
    // HTTP Server Implementation
    void HandleHTTPRequest(const FString& RequestBody);
    FString CreateJSONResponse(const FNavigationResponse& Response);
    FNavigationCommand ParseJSONCommand(const FString& JSONString);

    // Command Handlers
    FNavigationResponse HandleFocusAssetCommand(const FNavigationCommand& Command);
    FNavigationResponse HandleOpenAssetCommand(const FNavigationCommand& Command);
    FNavigationResponse HandleSearchCommand(const FNavigationCommand& Command);
    FNavigationResponse HandleNavigateCommand(const FNavigationCommand& Command);
    FNavigationResponse HandleBlueprintCommand(const FNavigationCommand& Command);

    // Helper Methods
    UObject* FindAssetByName(const FString& AssetName);
    void ShowNotification(const FString& Message, bool bSuccess);
    bool ValidateCommand(const FNavigationCommand& Command, FString& OutError);

private:
    // Server State
    UPROPERTY()
    bool bServerRunning;

    UPROPERTY()
    int32 ServerPort;

    // Navigation History
    UPROPERTY()
    TArray<FString> BreadcrumbHistory;

    UPROPERTY()
    TMap<FString, FString> SessionCache;

    // HTTP Server Handle (implementation specific)
    TSharedPtr<class FHttpServerModule> HttpServerModule;
    TSharedPtr<class IHttpRouter> HttpRouter;
};
