package io.homeassistant.companion.android.demo

import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DemoWebViewContent @Inject constructor(
    private val demoEntityRepository: DemoEntityRepository
) {

    fun generateDemoHTML(): String {
        val entities = demoEntityRepository.getEntities()
        
        val entityCards = entities.joinToString("\n") { entity ->
            val domain = entity.entityId.split(".")[0]
            when (domain) {
                "light", "switch" -> generateControlCard(entity)
                "sensor" -> generateSensorCard(entity)
                "binary_sensor" -> generateBinarySensorCard(entity)
                "climate" -> generateClimateCard(entity)
                "lock" -> generateLockCard(entity)
                else -> generateGenericCard(entity)
            }
        }

        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Assistant Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
        }
        
        .card h3 {
            color: #2c3e50;
            margin-bottom: 16px;
            font-size: 1.3rem;
            font-weight: 500;
        }
        
        .control-button {
            width: 100%;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .control-button.on {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
        }
        
        .control-button.off {
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
        }
        
        .control-button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        .sensor-value {
            font-size: 2rem;
            font-weight: 300;
            color: #3498db;
            text-align: center;
            margin: 16px 0;
        }
        
        .unit {
            font-size: 1rem;
            color: #7f8c8d;
            margin-left: 8px;
        }
        
        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status.on {
            background: #e8f5e8;
            color: #2e7d32;
        }
        
        .status.off {
            background: #ffebee;
            color: #c62828;
        }
        
        .demo-notice {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 193, 7, 0.9);
            color: #856404;
            padding: 12px 16px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 193, 7, 0.3);
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .dashboard {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            
            .card {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="demo-notice">
        🎭 Demo Mode Active
    </div>
    
    <div class="header">
        <h1>🏠 Home Assistant</h1>
        <p>Demo Dashboard - Experience smart home control</p>
    </div>
    
    <div class="dashboard">
        $entityCards
    </div>
    
    <script>
        function toggleEntity(entityId, currentState) {
            const newState = currentState === 'on' ? 'off' : 'on';
            
            // Simulate API call to Home Assistant
            if (window.externalApp && window.externalApp.externalBus) {
                const message = JSON.stringify({
                    type: 'call_service',
                    domain: entityId.split('.')[0],
                    service: newState === 'on' ? 'turn_on' : 'turn_off',
                    service_data: { entity_id: entityId }
                });
                window.externalApp.externalBus(message);
            }
            
            // Update UI immediately for demo responsiveness
            const button = document.querySelector(`[data-entity-id="${'$'}entityId"]`);
            if (button) {
                button.className = `control-button ${'$'}{newState}`;
                button.textContent = newState.toUpperCase();
                button.setAttribute('onclick', `toggleEntity('${'$'}entityId', '${'$'}{newState}')`);
            }
        }
        
        // Simulate some dynamic updates
        setInterval(() => {
            // Update temperature sensor with slight variations
            const tempElement = document.querySelector('[data-sensor="temperature"]');
            if (tempElement) {
                const currentTemp = parseFloat(tempElement.textContent);
                const newTemp = (currentTemp + (Math.random() - 0.5) * 0.2).toFixed(1);
                tempElement.textContent = newTemp;
            }
            
            // Update humidity sensor
            const humidityElement = document.querySelector('[data-sensor="humidity"]');
            if (humidityElement) {
                const currentHumidity = parseInt(humidityElement.textContent);
                const newHumidity = Math.max(35, Math.min(65, currentHumidity + Math.floor((Math.random() - 0.5) * 3)));
                humidityElement.textContent = newHumidity;
            }
        }, 5000);
        
        // Simulate connection status
        document.addEventListener('DOMContentLoaded', function() {
            if (window.externalApp && window.externalApp.externalBus) {
                // Notify that we're connected
                const connectionMessage = JSON.stringify({
                    type: 'connection-status',
                    payload: { event: 'connected' }
                });
                window.externalApp.externalBus(connectionMessage);
            }
        });
    </script>
</body>
</html>
        """.trimIndent()
    }
    
    private fun generateControlCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        val state = entity.state
        val domain = entity.entityId.split(".")[0]
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <button class="control-button $state" 
                    data-entity-id="${entity.entityId}"
                    onclick="toggleEntity('${entity.entityId}', '$state')">
                ${state.uppercase()}
            </button>
        </div>
        """
    }
    
    private fun generateSensorCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        val unit = entity.attributes["unit_of_measurement"] as? String ?: ""
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <div class="sensor-value">
                <span data-sensor="${entity.entityId.substringAfter(".")}">${entity.state}</span>
                <span class="unit">$unit</span>
            </div>
        </div>
        """
    }
    
    private fun generateBinarySensorCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        val state = entity.state
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <div style="text-align: center; padding: 20px 0;">
                <span class="status $state">${if (state == "on") "OPEN" else "CLOSED"}</span>
            </div>
        </div>
        """
    }
    
    private fun generateClimateCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        val currentTemp = entity.attributes["current_temperature"] as? Number ?: 0
        val targetTemp = entity.attributes["temperature"] as? Number ?: 0
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <div class="sensor-value">
                ${currentTemp}°C
            </div>
            <p style="text-align: center; color: #7f8c8d;">Target: ${targetTemp}°C</p>
        </div>
        """
    }
    
    private fun generateLockCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        val state = entity.state
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <div style="text-align: center; padding: 20px 0;">
                <span class="status ${if (state == "locked") "off" else "on"}">${state.uppercase()}</span>
            </div>
        </div>
        """
    }
    
    private fun generateGenericCard(entity: Entity): String {
        val friendlyName = entity.attributes["friendly_name"] as? String ?: entity.entityId
        
        return """
        <div class="card">
            <h3>$friendlyName</h3>
            <p style="text-align: center; color: #7f8c8d;">${entity.state}</p>
        </div>
        """
    }
}