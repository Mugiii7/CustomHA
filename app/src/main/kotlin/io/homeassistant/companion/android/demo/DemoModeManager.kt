package io.homeassistant.companion.android.demo

import android.content.Context
import android.content.SharedPreferences
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DemoModeManager @Inject constructor(
    private val context: Context
) {
    companion object {
        private const val PREFS_NAME = "demo_mode_prefs"
        private const val KEY_DEMO_MODE_ENABLED = "demo_mode_enabled"
        const val DEMO_SERVER_ID = -999
        const val DEMO_SERVER_URL = "http://demo.home-assistant.local"
        const val DEMO_SERVER_NAME = "Demo Home"
    }

    private val sharedPrefs: SharedPreferences by lazy {
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    var isDemoModeEnabled: Boolean
        get() = sharedPrefs.getBoolean(KEY_DEMO_MODE_ENABLED, false)
        set(value) = sharedPrefs.edit().putBoolean(KEY_DEMO_MODE_ENABLED, value).apply()

    fun enableDemoMode() {
        isDemoModeEnabled = true
    }

    fun disableDemoMode() {
        isDemoModeEnabled = false
    }

    fun getDemoServerName(): String = DEMO_SERVER_NAME
}