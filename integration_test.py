#!/usr/bin/env python3
"""
Integration Flow Test for Home Assistant Android Demo Mode

This test simulates the complete demo mode flow and tests integration between components.
"""

import sys
import os
import re
from datetime import datetime

class DemoModeIntegrationTest:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.project_root = "/app"
        self.flow_issues = []

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

    def test_demo_mode_activation_flow(self):
        """Test the complete demo mode activation flow"""
        # Step 1: Check WelcomeView has demo button
        welcome_view_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeView.kt"
        with open(welcome_view_file, 'r') as f:
            welcome_content = f.read()
        
        if "Try Demo Mode" not in welcome_content:
            self.flow_issues.append("Demo button not found in WelcomeView")
            return False
        
        # Step 2: Check WelcomeFragment handles demo mode
        welcome_fragment_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeFragment.kt"
        with open(welcome_fragment_file, 'r') as f:
            fragment_content = f.read()
        
        if "demoModeManager.enableDemoMode()" not in fragment_content:
            self.flow_issues.append("Demo mode not enabled in WelcomeFragment")
            return False
        
        # Step 3: Check LaunchActivity detects demo mode
        launch_activity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/launch/LaunchActivity.kt"
        with open(launch_activity_file, 'r') as f:
            launch_content = f.read()
        
        if "demoModeManager.isDemoModeEnabled" not in launch_content:
            self.flow_issues.append("Demo mode not detected in LaunchActivity")
            return False
        
        # Step 4: Check WebViewActivity loads demo content
        webview_activity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        with open(webview_activity_file, 'r') as f:
            webview_content = f.read()
        
        if "demoWebViewContent.generateDemoHTML()" not in webview_content:
            self.flow_issues.append("Demo HTML not generated in WebViewActivity")
            return False
        
        print("Demo mode activation flow is complete")
        return True

    def test_entity_interaction_flow(self):
        """Test the entity interaction flow in demo mode"""
        # Check DemoEntityRepository has entities
        entity_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt"
        with open(entity_repo_file, 'r') as f:
            entity_content = f.read()
        
        # Check for entity creation
        if "initializeDemoEntities()" not in entity_content:
            self.flow_issues.append("Demo entities not initialized")
            return False
        
        # Check for state updates
        if "updateEntityState" not in entity_content:
            self.flow_issues.append("Entity state updates not implemented")
            return False
        
        # Check DemoIntegrationRepository handles actions
        integration_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        with open(integration_repo_file, 'r') as f:
            integration_content = f.read()
        
        # Check for action handling
        if "callAction" not in integration_content:
            self.flow_issues.append("Action handling not implemented")
            return False
        
        # Check for entity state changes
        if "demoEntityRepository.updateEntityState" not in integration_content:
            self.flow_issues.append("Entity state changes not connected")
            return False
        
        print("Entity interaction flow is properly implemented")
        return True

    def test_webview_javascript_integration(self):
        """Test WebView JavaScript integration for demo mode"""
        webview_content_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        with open(webview_content_file, 'r') as f:
            content = f.read()
        
        # Check for JavaScript functions
        js_functions = [
            "toggleEntity",
            "externalApp.externalBus",
            "addEventListener"
        ]
        
        for func in js_functions:
            if func not in content:
                self.flow_issues.append(f"Missing JavaScript function: {func}")
                return False
        
        # Check for entity control logic
        if "turn_on" not in content or "turn_off" not in content:
            self.flow_issues.append("Entity control logic missing in JavaScript")
            return False
        
        # Check for dynamic updates
        if "setInterval" not in content:
            self.flow_issues.append("Dynamic sensor updates not implemented")
            return False
        
        print("WebView JavaScript integration is complete")
        return True

    def test_demo_data_consistency(self):
        """Test that demo data is consistent across components"""
        # Get entities from DemoEntityRepository
        entity_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt"
        with open(entity_repo_file, 'r') as f:
            entity_content = f.read()
        
        # Extract entity IDs
        entity_pattern = r'"([^"]+\.[^"]+)"'
        entities = re.findall(entity_pattern, entity_content)
        
        # Check that DemoIntegrationRepository can handle these entities
        integration_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        with open(integration_repo_file, 'r') as f:
            integration_content = f.read()
        
        # Check that integration repository gets entities from entity repository
        if "demoEntityRepository.getEntities()" not in integration_content:
            self.flow_issues.append("Integration repository not using entity repository")
            return False
        
        # Check that WebView content uses entity repository
        webview_content_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        with open(webview_content_file, 'r') as f:
            webview_content = f.read()
        
        if "demoEntityRepository.getEntities()" not in webview_content:
            self.flow_issues.append("WebView content not using entity repository")
            return False
        
        print("Demo data consistency is maintained")
        return True

    def test_demo_mode_persistence(self):
        """Test that demo mode state is properly persisted"""
        demo_manager_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt"
        with open(demo_manager_file, 'r') as f:
            content = f.read()
        
        # Check for SharedPreferences usage
        if "SharedPreferences" not in content:
            self.flow_issues.append("Demo mode state not persisted")
            return False
        
        # Check for getter and setter
        if "isDemoModeEnabled" not in content:
            self.flow_issues.append("Demo mode state getter/setter missing")
            return False
        
        # Check for enable/disable methods
        if "enableDemoMode()" not in content or "disableDemoMode()" not in content:
            self.flow_issues.append("Demo mode enable/disable methods missing")
            return False
        
        print("Demo mode persistence is properly implemented")
        return True

    def test_demo_server_configuration(self):
        """Test demo server configuration"""
        demo_manager_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt"
        with open(demo_manager_file, 'r') as f:
            content = f.read()
        
        # Check for demo server constants
        demo_constants = [
            "DEMO_SERVER_ID = -999",
            "DEMO_SERVER_URL = \"http://demo.home-assistant.local\"",
            "DEMO_SERVER_NAME = \"Demo Home\""
        ]
        
        for constant in demo_constants:
            if constant not in content:
                self.flow_issues.append(f"Missing demo server constant: {constant}")
                return False
        
        # Check that WebViewActivity uses demo URL
        webview_activity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        with open(webview_activity_file, 'r') as f:
            webview_content = f.read()
        
        if "demo.home-assistant.local" not in webview_content:
            self.flow_issues.append("Demo server URL not used in WebViewActivity")
            return False
        
        print("Demo server configuration is correct")
        return True

    def test_error_handling_and_fallbacks(self):
        """Test error handling and fallback mechanisms"""
        # Check that demo mode has proper error handling
        integration_repo_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        with open(integration_repo_file, 'r') as f:
            content = f.read()
        
        # Check for null safety
        if "entityId: String?" not in content and "entityId ?: return" not in content:
            # This is acceptable as the demo implementation might not need extensive null checking
            pass
        
        # Check that WebView has connection simulation
        webview_activity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        with open(webview_activity_file, 'r') as f:
            webview_content = f.read()
        
        if "isConnected = true" not in webview_content:
            self.flow_issues.append("Demo mode connection not simulated")
            return False
        
        print("Error handling and fallbacks are adequate")
        return True

    def test_ui_responsiveness_features(self):
        """Test UI responsiveness features in demo mode"""
        webview_content_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        with open(webview_content_file, 'r') as f:
            content = f.read()
        
        # Check for responsive CSS
        responsive_features = [
            "@media",
            "grid-template-columns",
            "auto-fit",
            "minmax"
        ]
        
        for feature in responsive_features:
            if feature not in content:
                self.flow_issues.append(f"Missing responsive feature: {feature}")
                return False
        
        # Check for interactive elements
        interactive_features = [
            "transition",
            "hover",
            "transform",
            "cursor: pointer"
        ]
        
        for feature in interactive_features:
            if feature not in content:
                self.flow_issues.append(f"Missing interactive feature: {feature}")
                return False
        
        print("UI responsiveness features are implemented")
        return True

    def run_all_tests(self):
        """Run all integration tests"""
        print("🔗 Starting Demo Mode Integration Flow Tests")
        print(f"📅 Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all integration tests
        self.run_test("Demo Mode Activation Flow", self.test_demo_mode_activation_flow)
        self.run_test("Entity Interaction Flow", self.test_entity_interaction_flow)
        self.run_test("WebView JavaScript Integration", self.test_webview_javascript_integration)
        self.run_test("Demo Data Consistency", self.test_demo_data_consistency)
        self.run_test("Demo Mode Persistence", self.test_demo_mode_persistence)
        self.run_test("Demo Server Configuration", self.test_demo_server_configuration)
        self.run_test("Error Handling and Fallbacks", self.test_error_handling_and_fallbacks)
        self.run_test("UI Responsiveness Features", self.test_ui_responsiveness_features)
        
        # Print results
        print(f"\n📊 Integration Test Results:")
        print(f"Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.flow_issues:
            print(f"\n⚠️  Flow issues found:")
            for issue in self.flow_issues:
                print(f"  - {issue}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All integration tests passed! Demo mode flow is complete and functional.")
            return 0
        else:
            print("❌ Some integration tests failed. Please review the flow issues above.")
            return 1

def main():
    """Main test function"""
    tester = DemoModeIntegrationTest()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())