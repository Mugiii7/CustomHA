package io.homeassistant.companion.android.demo

import io.homeassistant.companion.android.common.data.integration.Entity
import java.time.LocalDateTime
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DemoEntityRepository @Inject constructor() {

    private val _entities = mutableMapOf<String, Entity>()

    init {
        initializeDemoEntities()
    }

    fun getEntities(): List<Entity> = _entities.values.toList()

    fun getEntity(entityId: String): Entity? = _entities[entityId]

    fun updateEntityState(entityId: String, newState: String) {
        _entities[entityId]?.let { entity ->
            _entities[entityId] = entity.copy(
                state = newState,
                lastChanged = LocalDateTime.now(),
                lastUpdated = LocalDateTime.now()
            )
        }
    }

    private fun initializeDemoEntities() {
        val now = LocalDateTime.now()

        // Demo lights
        _entities["light.living_room"] = Entity(
            entityId = "light.living_room",
            state = "off",
            attributes = mapOf(
                "friendly_name" to "Living Room Light",
                "supported_features" to 1,
                "brightness" to 255
            ),
            lastChanged = now,
            lastUpdated = now
        )

        _entities["light.bedroom"] = Entity(
            entityId = "light.bedroom",
            state = "on",
            attributes = mapOf(
                "friendly_name" to "Bedroom Light",
                "supported_features" to 1,
                "brightness" to 180
            ),
            lastChanged = now,
            lastUpdated = now
        )

        _entities["light.kitchen"] = Entity(
            entityId = "light.kitchen",
            state = "off",
            attributes = mapOf(
                "friendly_name" to "Kitchen Light",
                "supported_features" to 1,
                "brightness" to 255
            ),
            lastChanged = now,
            lastUpdated = now
        )

        // Demo switches
        _entities["switch.porch_light"] = Entity(
            entityId = "switch.porch_light",
            state = "on",
            attributes = mapOf(
                "friendly_name" to "Porch Light",
                "device_class" to "switch"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        _entities["switch.coffee_maker"] = Entity(
            entityId = "switch.coffee_maker",
            state = "off",
            attributes = mapOf(
                "friendly_name" to "Coffee Maker",
                "device_class" to "outlet"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        // Demo sensors
        _entities["sensor.temperature"] = Entity(
            entityId = "sensor.temperature",
            state = "21.5",
            attributes = mapOf(
                "friendly_name" to "Living Room Temperature",
                "unit_of_measurement" to "°C",
                "device_class" to "temperature"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        _entities["sensor.humidity"] = Entity(
            entityId = "sensor.humidity",
            state = "45",
            attributes = mapOf(
                "friendly_name" to "Living Room Humidity",
                "unit_of_measurement" to "%",
                "device_class" to "humidity"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        // Demo binary sensors
        _entities["binary_sensor.front_door"] = Entity(
            entityId = "binary_sensor.front_door",
            state = "off",
            attributes = mapOf(
                "friendly_name" to "Front Door",
                "device_class" to "door"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        _entities["binary_sensor.motion_living_room"] = Entity(
            entityId = "binary_sensor.motion_living_room",
            state = "off",
            attributes = mapOf(
                "friendly_name" to "Living Room Motion",
                "device_class" to "motion"
            ),
            lastChanged = now,
            lastUpdated = now
        )

        // Demo climate
        _entities["climate.living_room"] = Entity(
            entityId = "climate.living_room",
            state = "heat",
            attributes = mapOf(
                "friendly_name" to "Living Room Thermostat",
                "temperature" to 21,
                "target_temp_low" to 18,
                "target_temp_high" to 24,
                "current_temperature" to 21.5,
                "hvac_modes" to listOf("off", "heat", "cool", "auto")
            ),
            lastChanged = now,
            lastUpdated = now
        )

        // Demo lock
        _entities["lock.front_door"] = Entity(
            entityId = "lock.front_door",
            state = "locked",
            attributes = mapOf(
                "friendly_name" to "Front Door Lock"
            ),
            lastChanged = now,
            lastUpdated = now
        )
    }
}