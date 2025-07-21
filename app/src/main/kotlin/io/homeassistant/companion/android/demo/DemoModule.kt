package io.homeassistant.companion.android.demo

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
class DemoModule {

    @Provides
    @Singleton
    fun provideDemoEntityRepository(): DemoEntityRepository = DemoEntityRepository()

    @Provides
    @Singleton
    fun provideDemoIntegrationRepository(demoEntityRepository: DemoEntityRepository): DemoIntegrationRepository =
        DemoIntegrationRepository(demoEntityRepository)

    @Provides
    @Singleton
    fun provideDemoWebViewContent(demoEntityRepository: DemoEntityRepository): DemoWebViewContent =
        DemoWebViewContent(demoEntityRepository)
}