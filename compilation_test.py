#!/usr/bin/env python3
"""
Advanced Compilation Test for Home Assistant Android Demo Mode

This test performs deeper analysis of the code to identify potential compilation issues.
"""

import sys
import os
import re
from datetime import datetime

class AndroidCompilationTest:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.project_root = "/app"
        self.issues_found = []

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
            else:
                print(f"❌ Failed - {name}")
            return result
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            return False

    def test_import_consistency(self):
        """Test that all demo-related imports are consistent"""
        demo_files = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        ]
        
        # Check that demo files have proper package declarations
        for file_path in demo_files:
            with open(file_path, 'r') as f:
                content = f.read()
            
            if "package io.homeassistant.companion.android.demo" not in content:
                self.issues_found.append(f"Incorrect package declaration in {file_path}")
                return False
        
        # Check that files importing demo classes use correct imports
        importing_files = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/launch/LaunchActivity.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeFragment.kt"
        ]
        
        for file_path in importing_files:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for proper demo imports
            if "DemoModeManager" in content and "import io.homeassistant.companion.android.demo.DemoModeManager" not in content:
                self.issues_found.append(f"Missing DemoModeManager import in {file_path}")
                return False
        
        print("All imports are consistent")
        return True

    def test_dependency_injection_annotations(self):
        """Test that dependency injection annotations are properly used"""
        files_with_injection = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        ]
        
        for file_path in files_with_injection:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for @Singleton or @Inject annotations
            if "@Singleton" not in content and "@Inject" not in content:
                self.issues_found.append(f"Missing dependency injection annotations in {file_path}")
                return False
        
        print("Dependency injection annotations are properly used")
        return True

    def test_kotlin_syntax_basics(self):
        """Test basic Kotlin syntax in demo files"""
        demo_files = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        ]
        
        for file_path in demo_files:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for basic syntax issues
            if content.count('{') != content.count('}'):
                self.issues_found.append(f"Mismatched braces in {file_path}")
                return False
            
            if content.count('(') != content.count(')'):
                self.issues_found.append(f"Mismatched parentheses in {file_path}")
                return False
            
            # Check for proper class declarations
            if "class " in content and not re.search(r'class\s+\w+', content):
                self.issues_found.append(f"Invalid class declaration in {file_path}")
                return False
        
        print("Basic Kotlin syntax appears correct")
        return True

    def test_entity_state_management(self):
        """Test that entity state management is properly implemented"""
        entity_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt"
        
        with open(entity_repo_file, 'r') as f:
            content = f.read()
        
        # Check for proper entity state updates
        if "updateEntityState" not in content:
            self.issues_found.append("Missing updateEntityState method")
            return False
        
        # Check for proper entity initialization
        if "initializeDemoEntities" not in content:
            self.issues_found.append("Missing initializeDemoEntities method")
            return False
        
        # Check for LocalDateTime usage
        if "LocalDateTime" not in content:
            self.issues_found.append("Missing LocalDateTime for entity timestamps")
            return False
        
        print("Entity state management is properly implemented")
        return True

    def test_webview_integration(self):
        """Test WebView integration for demo mode"""
        webview_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        
        with open(webview_file, 'r') as f:
            content = f.read()
        
        # Check for proper demo mode detection
        if "demoModeManager.isDemoModeEnabled" not in content:
            self.issues_found.append("Missing demo mode detection in WebViewActivity")
            return False
        
        # Check for demo HTML loading
        if "loadDataWithBaseURL" not in content:
            self.issues_found.append("Missing loadDataWithBaseURL for demo content")
            return False
        
        # Check for demo base URL
        if "demo.home-assistant.local" not in content:
            self.issues_found.append("Missing demo base URL")
            return False
        
        print("WebView integration is properly implemented")
        return True

    def test_html_generation_completeness(self):
        """Test that HTML generation is complete and valid"""
        webview_content_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        webview_activity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        
        with open(webview_content_file, 'r') as f:
            content = f.read()
        
        with open(webview_activity_file, 'r') as f:
            webview_content = f.read()
        
        # Check for complete HTML structure in DemoWebViewContent
        html_requirements = [
            "<!DOCTYPE html>",
            "<html",
            "<head>",
            "<body>",
            "</html>"
        ]
        
        for requirement in html_requirements:
            if requirement not in content:
                self.issues_found.append(f"Missing HTML requirement: {requirement}")
                return False
        
        # Check for MIME type and encoding in WebViewActivity
        webview_requirements = [
            "text/html",
            "UTF-8"
        ]
        
        for requirement in webview_requirements:
            if requirement not in webview_content:
                self.issues_found.append(f"Missing WebView requirement: {requirement}")
                return False
        
        # Check for JavaScript functionality
        js_requirements = [
            "toggleEntity",
            "externalApp",
            "externalBus",
            "addEventListener"
        ]
        
        for requirement in js_requirements:
            if requirement not in content:
                self.issues_found.append(f"Missing JavaScript requirement: {requirement}")
                return False
        
        print("HTML generation is complete and valid")
        return True

    def test_interface_implementation(self):
        """Test that DemoIntegrationRepository properly implements IntegrationRepository"""
        integration_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        
        with open(integration_file, 'r') as f:
            content = f.read()
        
        # Check for proper interface implementation
        if ": IntegrationRepository" not in content:
            self.issues_found.append("DemoIntegrationRepository does not implement IntegrationRepository")
            return False
        
        # Check for key method implementations
        required_methods = [
            "override suspend fun getEntities()",
            "override suspend fun getEntity(entityId: String)",
            "override suspend fun callAction",
            "override suspend fun registerDevice",
            "override suspend fun getConfig()"
        ]
        
        for method in required_methods:
            if method not in content:
                self.issues_found.append(f"Missing method implementation: {method}")
                return False
        
        print("Interface implementation is correct")
        return True

    def test_coroutine_usage(self):
        """Test that coroutines are properly used"""
        files_with_coroutines = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        ]
        
        for file_path in files_with_coroutines:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for proper suspend function usage
            if "suspend fun" in content:
                # Check for proper coroutine imports
                if "kotlinx.coroutines" not in content:
                    self.issues_found.append(f"Missing coroutine imports in {file_path}")
                    return False
        
        print("Coroutine usage is correct")
        return True

    def test_android_context_usage(self):
        """Test that Android Context is properly used"""
        demo_manager_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt"
        
        with open(demo_manager_file, 'r') as f:
            content = f.read()
        
        # Check for proper Context usage
        if "Context" not in content:
            self.issues_found.append("Missing Context import/usage in DemoModeManager")
            return False
        
        # Check for SharedPreferences usage
        if "SharedPreferences" not in content:
            self.issues_found.append("Missing SharedPreferences usage in DemoModeManager")
            return False
        
        print("Android Context usage is correct")
        return True

    def test_entity_action_simulation(self):
        """Test that entity actions are properly simulated"""
        integration_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        
        with open(integration_file, 'r') as f:
            content = f.read()
        
        # Check for action handling
        actions = ["turn_on", "turn_off", "toggle", "lock", "unlock"]
        
        for action in actions:
            if f'"{action}"' not in content:
                self.issues_found.append(f"Missing action simulation: {action}")
                return False
        
        # Check for domain handling
        domains = ["light", "switch"]
        
        for domain in domains:
            if f'"{domain}"' not in content:
                self.issues_found.append(f"Missing domain handling: {domain}")
                return False
        
        print("Entity action simulation is properly implemented")
        return True

    def run_all_tests(self):
        """Run all compilation tests"""
        print("🔧 Starting Advanced Compilation Tests for Android Demo Mode")
        print(f"📅 Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        self.run_test("Import Consistency", self.test_import_consistency)
        self.run_test("Dependency Injection Annotations", self.test_dependency_injection_annotations)
        self.run_test("Kotlin Syntax Basics", self.test_kotlin_syntax_basics)
        self.run_test("Entity State Management", self.test_entity_state_management)
        self.run_test("WebView Integration", self.test_webview_integration)
        self.run_test("HTML Generation Completeness", self.test_html_generation_completeness)
        self.run_test("Interface Implementation", self.test_interface_implementation)
        self.run_test("Coroutine Usage", self.test_coroutine_usage)
        self.run_test("Android Context Usage", self.test_android_context_usage)
        self.run_test("Entity Action Simulation", self.test_entity_action_simulation)
        
        # Print results
        print(f"\n📊 Advanced Test Results:")
        print(f"Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.issues_found:
            print(f"\n⚠️  Issues found:")
            for issue in self.issues_found:
                print(f"  - {issue}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All advanced tests passed! Code appears ready for compilation.")
            return 0
        else:
            print("❌ Some advanced tests failed. Please review the issues above.")
            return 1

def main():
    """Main test function"""
    tester = AndroidCompilationTest()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())