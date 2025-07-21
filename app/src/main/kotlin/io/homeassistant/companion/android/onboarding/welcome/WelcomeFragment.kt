package io.homeassistant.companion.android.onboarding.welcome

import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.compose.ui.platform.ComposeView
import androidx.fragment.app.Fragment
import dagger.hilt.android.AndroidEntryPoint
import io.homeassistant.companion.android.R
import io.homeassistant.companion.android.demo.DemoModeManager
import io.homeassistant.companion.android.onboarding.discovery.DiscoveryFragment
import io.homeassistant.companion.android.onboarding.manual.ManualSetupFragment
import io.homeassistant.companion.android.util.compose.HomeAssistantAppTheme
import io.homeassistant.companion.android.webview.WebViewActivity
import javax.inject.Inject

+@AndroidEntryPoint
class WelcomeFragment : Fragment() {

    @Inject
    lateinit var demoModeManager: DemoModeManager

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        return ComposeView(requireContext()).apply {
            setContent {
                HomeAssistantAppTheme {
                    WelcomeView(
                        onContinue = { welcomeNavigation() },
                        onDemoMode = { startDemoMode() }
                    )
                }
            }
        }
    }

    private fun welcomeNavigation() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            parentFragmentManager
                .beginTransaction()
                .replace(R.id.content, DiscoveryFragment::class.java, null)
                .addToBackStack("Welcome")
                .commit()
        } else {
            parentFragmentManager
                .beginTransaction()
                .replace(R.id.content, ManualSetupFragment::class.java, null)
                .addToBackStack("Welcome")
                .commit()
        }
    }

    private fun startDemoMode() {
        demoModeManager.enableDemoMode()
        
        // Start WebView directly with demo content
        startActivity(WebViewActivity.newInstance(requireContext()))
        requireActivity().finish()
    }
}
