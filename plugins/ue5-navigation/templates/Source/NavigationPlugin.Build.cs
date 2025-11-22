// ==========================================
// UE5 Navigation Plugin - Build.cs
// ==========================================

using UnrealBuildTool;

public class NavigationPlugin : ModuleRules
{
    public NavigationPlugin(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.AddRange(
            new string[] {
                // Add public include paths here
            }
        );

        PrivateIncludePaths.AddRange(
            new string[] {
                // Add private include paths here
            }
        );

        PublicDependencyModuleNames.AddRange(
            new string[]
            {
                "Core",
                "CoreUObject",
                "Engine",
                "InputCore",
                "HTTP",
                "HTTPServer",
                "Json",
                "JsonUtilities",
            }
        );

        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
                "UnrealEd",
                "EditorStyle",
                "LevelEditor",
                "Slate",
                "SlateCore",
                "AssetRegistry",
                "AssetTools",
                "ContentBrowser",
                "WorkspaceMenuStructure",
                "ToolMenus",
                "EditorSubsystem",
                "BlueprintGraph",
                "Kismet",
                "KismetCompiler",
                "SourceControl",
            }
        );

        DynamicallyLoadedModuleNames.AddRange(
            new string[]
            {
                // Add any modules that your module loads dynamically here
            }
        );

        // Enable RTTI for better type safety
        bEnableExceptions = true;
        bUseRTTI = true;
    }
}
