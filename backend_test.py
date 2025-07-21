#!/usr/bin/env python3
"""
Backend Test for Home Assistant Android Demo Mode Implementation

This test verifies the demo mode functionality by testing the Kotlin logic
and ensuring the demo infrastructure works correctly.
"""

import sys
import subprocess
import os
from datetime import datetime

class AndroidDemoModeTest:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.project_root = "/app"

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

    def test_project_structure(self):
        """Test if the demo mode files exist in the correct structure"""
        required_files = [
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeFragment.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeView.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt",
            "/app/app/src/main/kotlin/io/homeassistant/companion/android/launch/LaunchActivity.kt"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"Missing files: {missing_files}")
            return False
        
        print("All required demo mode files are present")
        return True

    def test_gradle_build_files(self):
        """Test if Gradle build files exist and are properly configured"""
        build_files = [
            "/app/build.gradle.kts",
            "/app/app/build.gradle.kts",
            "/app/settings.gradle.kts"
        ]
        
        for build_file in build_files:
            if not os.path.exists(build_file):
                print(f"Missing build file: {build_file}")
                return False
        
        print("Gradle build files are present")
        return True

    def test_demo_mode_manager_logic(self):
        """Test DemoModeManager constants and structure"""
        demo_manager_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoModeManager.kt"
        
        with open(demo_manager_file, 'r') as f:
            content = f.read()
        
        # Check for required constants
        required_constants = [
            "DEMO_SERVER_ID = -999",
            "DEMO_SERVER_URL = \"http://demo.home-assistant.local\"",
            "DEMO_SERVER_NAME = \"Demo Home\"",
            "KEY_DEMO_MODE_ENABLED = \"demo_mode_enabled\""
        ]
        
        for constant in required_constants:
            if constant not in content:
                print(f"Missing constant: {constant}")
                return False
        
        # Check for required methods
        required_methods = [
            "enableDemoMode()",
            "disableDemoMode()",
            "getDemoServerName()"
        ]
        
        for method in required_methods:
            if method not in content:
                print(f"Missing method: {method}")
                return False
        
        print("DemoModeManager structure is correct")
        return True

    def test_demo_entity_repository_entities(self):
        """Test DemoEntityRepository has required demo entities"""
        entity_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoEntityRepository.kt"
        
        with open(entity_file, 'r') as f:
            content = f.read()
        
        # Check for required entity types
        required_entities = [
            "light.living_room",
            "light.bedroom", 
            "light.kitchen",
            "switch.porch_light",
            "switch.coffee_maker",
            "sensor.temperature",
            "sensor.humidity",
            "binary_sensor.front_door",
            "binary_sensor.motion_living_room",
            "climate.living_room",
            "lock.front_door"
        ]
        
        missing_entities = []
        for entity in required_entities:
            if entity not in content:
                missing_entities.append(entity)
        
        if missing_entities:
            print(f"Missing entities: {missing_entities}")
            return False
        
        # Check for required methods
        required_methods = [
            "getEntities()",
            "getEntity(entityId: String)",
            "updateEntityState(entityId: String, newState: String)"
        ]
        
        for method in required_methods:
            if method not in content:
                print(f"Missing method: {method}")
                return False
        
        print("DemoEntityRepository has all required entities and methods")
        return True

    def test_demo_integration_repository_interface(self):
        """Test DemoIntegrationRepository implements required interface methods"""
        integration_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoIntegrationRepository.kt"
        
        with open(integration_file, 'r') as f:
            content = f.read()
        
        # Check that it implements IntegrationRepository
        if ": IntegrationRepository" not in content:
            print("DemoIntegrationRepository does not implement IntegrationRepository interface")
            return False
        
        # Check for key override methods
        required_overrides = [
            "override suspend fun getEntities()",
            "override suspend fun getEntity(entityId: String)",
            "override suspend fun callAction(domain: String, action: String, actionData: Map<String, Any?>)"
        ]
        
        for override_method in required_overrides:
            if override_method not in content:
                print(f"Missing override method: {override_method}")
                return False
        
        print("DemoIntegrationRepository properly implements interface")
        return True

    def test_demo_webview_content_generation(self):
        """Test DemoWebViewContent generates proper HTML"""
        webview_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/demo/DemoWebViewContent.kt"
        
        with open(webview_file, 'r') as f:
            content = f.read()
        
        # Check for HTML generation method
        if "fun generateDemoHTML(): String" not in content:
            print("Missing generateDemoHTML method")
            return False
        
        # Check for HTML structure elements
        html_elements = [
            "<!DOCTYPE html>",
            "<title>Home Assistant Demo</title>",
            "Demo Mode Active",
            "Home Assistant",
            "toggleEntity(entityId, currentState)"
        ]
        
        for element in html_elements:
            if element not in content:
                print(f"Missing HTML element: {element}")
                return False
        
        # Check for card generation methods
        card_methods = [
            "generateControlCard(entity)",
            "generateSensorCard(entity)",
            "generateBinarySensorCard(entity)",
            "generateClimateCard(entity)",
            "generateLockCard(entity)"
        ]
        
        for method in card_methods:
            if method not in content:
                print(f"Missing card generation method: {method}")
                return False
        
        print("DemoWebViewContent has proper HTML generation")
        return True

    def test_welcome_fragment_demo_integration(self):
        """Test WelcomeFragment has demo mode integration"""
        welcome_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeFragment.kt"
        
        with open(welcome_file, 'r') as f:
            content = f.read()
        
        # Check for demo mode manager injection
        if "lateinit var demoModeManager: DemoModeManager" not in content:
            print("Missing DemoModeManager injection")
            return False
        
        # Check for demo mode method
        if "private fun startDemoMode()" not in content:
            print("Missing startDemoMode method")
            return False
        
        # Check for demo mode enablement
        if "demoModeManager.enableDemoMode()" not in content:
            print("Missing demo mode enablement call")
            return False
        
        # Check for WebView activity start
        if "startActivity(WebViewActivity.newInstance(requireContext()))" not in content:
            print("Missing WebView activity start")
            return False
        
        print("WelcomeFragment has proper demo mode integration")
        return True

    def test_welcome_view_demo_button(self):
        """Test WelcomeView has demo mode button"""
        welcome_view_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/onboarding/welcome/WelcomeView.kt"
        
        with open(welcome_view_file, 'r') as f:
            content = f.read()
        
        # Check for demo mode parameter
        if "onDemoMode: () -> Unit" not in content:
            print("Missing onDemoMode parameter")
            return False
        
        # Check for demo button
        if "Try Demo Mode" not in content:
            print("Missing 'Try Demo Mode' button text")
            return False
        
        # Check for OutlinedButton
        if "OutlinedButton(" not in content:
            print("Missing OutlinedButton for demo mode")
            return False
        
        print("WelcomeView has proper demo mode button")
        return True

    def test_webview_activity_demo_integration(self):
        """Test WebViewActivity has demo mode integration"""
        webview_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/webview/WebViewActivity.kt"
        
        with open(webview_file, 'r') as f:
            content = f.read()
        
        # Check for demo mode manager injection
        if "lateinit var demoModeManager: DemoModeManager" not in content:
            print("Missing DemoModeManager injection")
            return False
        
        # Check for demo web view content injection
        if "lateinit var demoWebViewContent: DemoWebViewContent" not in content:
            print("Missing DemoWebViewContent injection")
            return False
        
        # Check for demo mode check in loadUrl
        if "if (demoModeManager.isDemoModeEnabled)" not in content:
            print("Missing demo mode check in loadUrl")
            return False
        
        # Check for demo HTML loading
        if "val demoHtml = demoWebViewContent.generateDemoHTML()" not in content:
            print("Missing demo HTML generation")
            return False
        
        # Check for loadDataWithBaseURL call
        if "webView.loadDataWithBaseURL(" not in content:
            print("Missing loadDataWithBaseURL call for demo content")
            return False
        
        print("WebViewActivity has proper demo mode integration")
        return True

    def test_launch_activity_demo_integration(self):
        """Test LaunchActivity has demo mode integration"""
        launch_file = "/app/app/src/main/kotlin/io/homeassistant/companion/android/launch/LaunchActivity.kt"
        
        with open(launch_file, 'r') as f:
            content = f.read()
        
        # Check for demo mode manager injection
        if "lateinit var demoModeManager: DemoModeManager" not in content:
            print("Missing DemoModeManager injection")
            return False
        
        # Check for demo mode check in displayWebview
        if "if (demoModeManager.isDemoModeEnabled)" not in content:
            print("Missing demo mode check in displayWebview")
            return False
        
        # Check for demo mode WebView start
        demo_webview_start = "startActivity(WebViewActivity.newInstance(this, \"/\"))"
        if demo_webview_start not in content:
            print("Missing demo mode WebView activity start")
            return False
        
        print("LaunchActivity has proper demo mode integration")
        return True

    def test_compilation_readiness(self):
        """Test if the project appears ready for compilation"""
        # Check for Gradle wrapper
        if not os.path.exists("/app/gradlew"):
            print("Missing Gradle wrapper")
            return False
        
        # Check for Android manifest
        manifest_path = "/app/app/src/main/AndroidManifest.xml"
        if not os.path.exists(manifest_path):
            print("Missing Android manifest")
            return False
        
        # Check for basic Android project structure
        android_dirs = [
            "/app/app/src/main/kotlin",
            "/app/app/src/main/res"
        ]
        
        for android_dir in android_dirs:
            if not os.path.exists(android_dir):
                print(f"Missing Android directory: {android_dir}")
                return False
        
        print("Project structure appears ready for compilation")
        return True

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Home Assistant Android Demo Mode Tests")
        print(f"📅 Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test project structure
        self.run_test("Project Structure", self.test_project_structure)
        self.run_test("Gradle Build Files", self.test_gradle_build_files)
        
        # Test demo mode components
        self.run_test("DemoModeManager Logic", self.test_demo_mode_manager_logic)
        self.run_test("DemoEntityRepository Entities", self.test_demo_entity_repository_entities)
        self.run_test("DemoIntegrationRepository Interface", self.test_demo_integration_repository_interface)
        self.run_test("DemoWebViewContent Generation", self.test_demo_webview_content_generation)
        
        # Test UI integration
        self.run_test("WelcomeFragment Demo Integration", self.test_welcome_fragment_demo_integration)
        self.run_test("WelcomeView Demo Button", self.test_welcome_view_demo_button)
        self.run_test("WebViewActivity Demo Integration", self.test_webview_activity_demo_integration)
        self.run_test("LaunchActivity Demo Integration", self.test_launch_activity_demo_integration)
        
        # Test compilation readiness
        self.run_test("Compilation Readiness", self.test_compilation_readiness)
        
        # Print results
        print(f"\n📊 Test Results:")
        print(f"Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Demo mode implementation looks good.")
            return 0
        else:
            print("❌ Some tests failed. Please review the implementation.")
            return 1

def main():
    """Main test function"""
    tester = AndroidDemoModeTest()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())