---
name: android-kotlin
description: Android Kotlin development with Coroutines, Jetpack Compose, Hilt, and MockK testing
---

# Android Kotlin Skill

*Load with: base.md*

---

## Project Structure

```
project/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── kotlin/com/example/app/
│   │   │   │   ├── data/               # Data layer
│   │   │   │   │   ├── local/          # Room database
│   │   │   │   │   ├── remote/         # Retrofit/Ktor services
│   │   │   │   │   └── repository/     # Repository implementations
│   │   │   │   ├── di/                 # Hilt modules
│   │   │   │   ├── domain/             # Business logic
│   │   │   │   │   ├── model/          # Domain models
│   │   │   │   │   ├── repository/     # Repository interfaces
│   │   │   │   │   └── usecase/        # Use cases
│   │   │   │   ├── ui/                 # Presentation layer
│   │   │   │   │   ├── feature/        # Feature screens
│   │   │   │   │   │   ├── FeatureScreen.kt      # Compose UI
│   │   │   │   │   │   └── FeatureViewModel.kt
│   │   │   │   │   ├── components/     # Reusable Compose components
│   │   │   │   │   └── theme/          # Material theme
│   │   │   │   └── App.kt              # Application class
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                       # Unit tests
│   │   └── androidTest/                # Instrumentation tests
│   └── build.gradle.kts
├── build.gradle.kts                    # Project-level build file
├── gradle.properties
├── settings.gradle.kts
└── CLAUDE.md
```

---

## Gradle Configuration (Kotlin DSL)

### App-level build.gradle.kts
```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.example.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }
}

dependencies {
    // Compose BOM
    val composeBom = platform("androidx.compose:compose-bom:2024.01.00")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // Hilt
    implementation("com.google.dagger:hilt-android:2.50")
    ksp("com.google.dagger:hilt-compiler:2.50")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")

    // Room
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")

    // Testing
    testImplementation("junit:junit:4.13.2")
    testImplementation("io.mockk:mockk:1.13.9")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    testImplementation("app.cash.turbine:turbine:1.0.0")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

---

## Kotlin Coroutines & Flow

### ViewModel with StateFlow
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    private val userId: String = checkNotNull(savedStateHandle["userId"])

    init {
        loadUser()
    }

    fun loadUser() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            getUserUseCase(userId)
                .catch { e ->
                    _uiState.update {
                        it.copy(isLoading = false, error = e.message)
                    }
                }
                .collect { user ->
                    _uiState.update {
                        it.copy(isLoading = false, user = user, error = null)
                    }
                }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}

data class UserUiState(
    val user: User? = null,
    val isLoading: Boolean = false,
    val error: String? = null
)
```

### Repository with Flow
```kotlin
interface UserRepository {
    fun getUser(userId: String): Flow<User>
    fun observeUsers(): Flow<List<User>>
    suspend fun saveUser(user: User)
}

class UserRepositoryImpl @Inject constructor(
    private val api: UserApi,
    private val dao: UserDao,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) : UserRepository {

    override fun getUser(userId: String): Flow<User> = flow {
        // Emit cached data first
        dao.getUserById(userId)?.let { emit(it) }

        // Fetch from network and update cache
        val remoteUser = api.getUser(userId)
        dao.insert(remoteUser)
        emit(remoteUser)
    }.flowOn(dispatcher)

    override fun observeUsers(): Flow<List<User>> =
        dao.observeAllUsers().flowOn(dispatcher)

    override suspend fun saveUser(user: User) = withContext(dispatcher) {
        api.saveUser(user)
        dao.insert(user)
    }
}
```

---

## Jetpack Compose

### Screen with ViewModel
```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel(),
    onNavigateBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserScreenContent(
        uiState = uiState,
        onRefresh = viewModel::loadUser,
        onErrorDismiss = viewModel::clearError,
        onNavigateBack = onNavigateBack
    )
}

@Composable
private fun UserScreenContent(
    uiState: UserUiState,
    onRefresh: () -> Unit,
    onErrorDismiss: () -> Unit,
    onNavigateBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("User Profile") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                uiState.user != null -> {
                    UserContent(user = uiState.user)
                }
            }

            uiState.error?.let { error ->
                Snackbar(
                    modifier = Modifier.align(Alignment.BottomCenter),
                    action = {
                        TextButton(onClick = onErrorDismiss) {
                            Text("Dismiss")
                        }
                    }
                ) {
                    Text(error)
                }
            }
        }
    }
}
```

---

## Sealed Classes for State

### Result Wrapper
```kotlin
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Error(val exception: Throwable) : Result<Nothing>
    data object Loading : Result<Nothing>
}

fun <T> Result<T>.getOrNull(): T? = (this as? Result.Success)?.data

inline fun <T, R> Result<T>.map(transform: (T) -> R): Result<R> = when (this) {
    is Result.Success -> Result.Success(transform(data))
    is Result.Error -> this
    is Result.Loading -> this
}
```

---

## Testing with MockK & Turbine

### ViewModel Tests
```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val getUserUseCase: GetUserUseCase = mockk()
    private val savedStateHandle = SavedStateHandle(mapOf("userId" to "123"))

    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        viewModel = UserViewModel(getUserUseCase, savedStateHandle)
    }

    @Test
    fun `loadUser success updates state with user`() = runTest {
        val user = User("123", "John Doe", "john@example.com")
        coEvery { getUserUseCase("123") } returns flowOf(user)

        viewModel.uiState.test {
            val initial = awaitItem()
            assertFalse(initial.isLoading)

            viewModel.loadUser()

            val loading = awaitItem()
            assertTrue(loading.isLoading)

            val success = awaitItem()
            assertFalse(success.isLoading)
            assertEquals(user, success.user)
        }
    }
}

class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(dispatcher)
    }
    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

---

## GitHub Actions

```yaml
name: Android Kotlin CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Run Detekt
        run: ./gradlew detekt

      - name: Run Ktlint
        run: ./gradlew ktlintCheck

      - name: Run Unit Tests
        run: ./gradlew testDebugUnitTest

      - name: Build Debug APK
        run: ./gradlew assembleDebug
```

---

## Lint Configuration

### detekt.yml
```yaml
build:
  maxIssues: 0

complexity:
  LongMethod:
    threshold: 20
  LongParameterList:
    functionThreshold: 4
  TooManyFunctions:
    thresholdInFiles: 10

style:
  MaxLineLength:
    maxLineLength: 120
  WildcardImport:
    active: true

coroutines:
  GlobalCoroutineUsage:
    active: true
```

---

## Kotlin Anti-Patterns

- ❌ **Blocking coroutines on Main** - Never use `runBlocking` on main thread
- ❌ **GlobalScope usage** - Use structured concurrency with viewModelScope/lifecycleScope
- ❌ **Collecting flows in init** - Use `repeatOnLifecycle` or `collectAsStateWithLifecycle`
- ❌ **Mutable state exposure** - Expose `StateFlow` not `MutableStateFlow`
- ❌ **Not handling exceptions in flows** - Always use `catch` operator
- ❌ **Lateinit for nullable** - Use `lazy` or nullable with `?`
- ❌ **Hardcoded dispatchers** - Inject dispatchers for testability
- ❌ **Not using sealed classes** - Prefer sealed for finite state sets
- ❌ **Side effects in Composables** - Use `LaunchedEffect`/`SideEffect`
- ❌ **Unstable Compose parameters** - Use stable/immutable types or `@Stable`

