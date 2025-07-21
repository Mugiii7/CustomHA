package io.homeassistant.companion.android.demo

import io.homeassistant.companion.android.common.data.integration.DeviceRegistration
import io.homeassistant.companion.android.common.data.integration.Entity
import io.homeassistant.companion.android.common.data.integration.IntegrationRepository
import io.homeassistant.companion.android.common.data.integration.SensorRegistration
import io.homeassistant.companion.android.common.data.integration.UpdateLocation
import io.homeassistant.companion.android.common.data.integration.impl.entities.RateLimitResponse
import io.homeassistant.companion.android.common.data.websocket.impl.entities.AssistPipelineEvent
import io.homeassistant.companion.android.common.data.websocket.impl.entities.GetConfigResponse
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf
import javax.inject.Inject

class DemoIntegrationRepository @Inject constructor(
    private val demoEntityRepository: DemoEntityRepository
) : IntegrationRepository {

    override suspend fun registerDevice(deviceRegistration: DeviceRegistration) {
        // Demo mode - no actual registration needed
    }

    override suspend fun updateRegistration(deviceRegistration: DeviceRegistration, allowReregistration: Boolean) {
        // Demo mode - no actual registration needed
    }

    override suspend fun getRegistration(): DeviceRegistration {
        return DeviceRegistration(
            appVersion = "Demo Version",
            deviceName = "Demo Device",
            pushToken = "demo_token"
        )
    }

    override suspend fun deletePreferences() {
        // Demo mode - nothing to delete
    }

    override suspend fun getNotificationRateLimits(): RateLimitResponse {
        return RateLimitResponse(successful = 100, errors = 0, total = 100, maximum = 100, remaining = 100, resetsAt = null)
    }

    override suspend fun renderTemplate(template: String, variables: Map<String, String>): String? {
        return "Demo Template Result"
    }

    override suspend fun getTemplateUpdates(template: String): Flow<String?>? {
        return flowOf("Demo Template Update")
    }

    override suspend fun updateLocation(updateLocation: UpdateLocation) {
        // Demo mode - no location update needed
    }

    override suspend fun getZones(): List<Entity> {
        return listOf(
            Entity(
                entityId = "zone.home",
                state = "zoning",
                attributes = mapOf(
                    "friendly_name" to "Home",
                    "latitude" to 0.0,
                    "longitude" to 0.0,
                    "radius" to 100
                ),
                lastChanged = java.time.LocalDateTime.now(),
                lastUpdated = java.time.LocalDateTime.now()
            )
        )
    }

    override suspend fun isAppLocked(): Boolean = false

    override suspend fun setAppActive(active: Boolean) {
        // Demo mode - no app active state needed
    }

    override suspend fun sessionTimeOut(value: Int) {
        // Demo mode - no timeout needed
    }

    override suspend fun getSessionTimeOut(): Int = 0

    override suspend fun setSessionExpireMillis(value: Long) {
        // Demo mode - no session expiration needed
    }

    override suspend fun getHomeAssistantVersion(): String = "2025.3.0"

    override suspend fun isHomeAssistantVersionAtLeast(year: Int, month: Int, release: Int): Boolean = true

    override suspend fun getConfig(): GetConfigResponse {
        return GetConfigResponse(
            components = listOf("light", "switch", "sensor", "binary_sensor", "climate", "lock"),
            configDir = "/config",
            elevation = 0,
            latitude = 0.0,
            longitude = 0.0,
            locationName = "Demo Home",
            timeZone = "UTC",
            unitSystem = mapOf("length" to "km", "mass" to "kg", "temperature" to "°C", "volume" to "L"),
            version = "2025.3.0",
            whitelist_external_dirs = emptyList()
        )
    }

    override suspend fun getServices(): List<io.homeassistant.companion.android.common.data.integration.Action>? {
        return emptyList()
    }

    override suspend fun getEntities(): List<Entity>? {
        return demoEntityRepository.getEntities()
    }

    override suspend fun getEntity(entityId: String): Entity? {
        return demoEntityRepository.getEntity(entityId)
    }

    override suspend fun getEntityUpdates(): Flow<Entity>? = null

    override suspend fun getEntityUpdates(entityIds: List<String>): Flow<Entity>? = null

    override suspend fun callAction(domain: String, action: String, actionData: Map<String, Any?>) {
        val entityId = actionData["entity_id"] as? String ?: return
        
        // Simulate entity state changes based on actions
        when (action) {
            "turn_on" -> {
                when (domain) {
                    "light", "switch" -> demoEntityRepository.updateEntityState(entityId, "on")
                }
            }
            "turn_off" -> {
                when (domain) {
                    "light", "switch" -> demoEntityRepository.updateEntityState(entityId, "off")
                }
            }
            "toggle" -> {
                val currentEntity = demoEntityRepository.getEntity(entityId)
                val newState = if (currentEntity?.state == "on") "off" else "on"
                demoEntityRepository.updateEntityState(entityId, newState)
            }
            "lock" -> demoEntityRepository.updateEntityState(entityId, "locked")
            "unlock" -> demoEntityRepository.updateEntityState(entityId, "unlocked")
        }
    }

    override suspend fun scanTag(data: Map<String, String>) {
        // Demo mode - no tag scanning needed
    }

    override suspend fun fireEvent(eventType: String, eventData: Map<String, Any>) {
        // Demo mode - no event firing needed
    }

    override suspend fun registerSensor(sensorRegistration: SensorRegistration<Any>) {
        // Demo mode - no sensor registration needed
    }

    override suspend fun updateSensors(sensors: List<SensorRegistration<Any>>): Boolean = true

    override suspend fun isTrusted(): Boolean = true

    override suspend fun setTrusted(trusted: Boolean) {
        // Demo mode - always trusted
    }

    override suspend fun shouldNotifySecurityWarning(): Boolean = false

    override suspend fun getAssistResponse(
        text: String,
        pipelineId: String?,
        conversationId: String?
    ): Flow<AssistPipelineEvent>? = null

    override suspend fun getLastUsedPipelineId(): String? = null

    override suspend fun getLastUsedPipelineSttSupport(): Boolean = false

    override suspend fun setLastUsedPipeline(pipelineId: String, supportsStt: Boolean) {
        // Demo mode - no pipeline needed
    }

    override suspend fun getThreadBorderAgentIds(): List<String> = emptyList()

    override suspend fun setThreadBorderAgentIds(ids: List<String>) {
        // Demo mode - no thread agents needed
    }

    override suspend fun getOrphanedThreadBorderAgentIds(): List<String> = emptyList()

    override suspend fun clearOrphanedThreadBorderAgentIds() {
        // Demo mode - no thread agents to clear
    }
}