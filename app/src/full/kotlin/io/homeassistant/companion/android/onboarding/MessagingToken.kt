package io.homeassistant.companion.android.onboarding

import timber.log.Timber

/**
 * Stub implementation for Firebase messaging token.
 * Firebase services are disabled in this build.
 * Returns empty string to maintain compatibility.
 */
suspend fun getMessagingToken(): String {
    Timber.d("Firebase services disabled - returning empty messaging token")
    return ""
}