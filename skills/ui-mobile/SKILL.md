---
name: ui-mobile
description: Mobile UI patterns - React Native, iOS/Android, touch targets
---

# Mobile UI Design Skill (React Native)

*Load with: base.md + react-native.md*

---

## MANDATORY: Mobile Accessibility Standards

**These rules are NON-NEGOTIABLE. Every UI element must pass these checks.**

### 1. Touch Targets (CRITICAL)
```typescript
// MINIMUM 44x44 points for ALL interactive elements
const MINIMUM_TOUCH_SIZE = 44;

// EVERY button, link, icon button must meet this
const styles = StyleSheet.create({
  button: {
    minHeight: MINIMUM_TOUCH_SIZE,
    minWidth: MINIMUM_TOUCH_SIZE,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  iconButton: {
    width: MINIMUM_TOUCH_SIZE,
    height: MINIMUM_TOUCH_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

// NEVER DO THIS:
style={{ height: 30 }}  // ✗ TOO SMALL
style={{ padding: 4 }}  // ✗ RESULTS IN TINY TARGET
```

### 2. Color Contrast (CRITICAL)
```typescript
// WCAG 2.1 AA: 4.5:1 for text, 3:1 for large text/UI

// SAFE COMBINATIONS:
const colors = {
  // Light mode
  textPrimary: '#000000',     // on white = 21:1 ✓
  textSecondary: '#374151',   // gray-700 on white = 9.2:1 ✓

  // Dark mode
  textPrimaryDark: '#FFFFFF', // on gray-900 = 16:1 ✓
  textSecondaryDark: '#E5E7EB', // gray-200 on gray-900 = 11:1 ✓
};

// FORBIDDEN - FAILS CONTRAST:
// ✗ '#9CA3AF' (gray-400) on white = 2.6:1
// ✗ '#6B7280' (gray-500) on '#111827' = 4.0:1
// ✗ Any text below 4.5:1 ratio
```

### 3. Visibility Rules
```typescript
// ALL BUTTONS MUST HAVE visible boundaries

// PRIMARY: Solid background with contrasting text
<Pressable style={styles.primaryButton}>
  <Text style={{ color: '#FFFFFF' }}>Submit</Text>
</Pressable>

const styles = StyleSheet.create({
  primaryButton: {
    backgroundColor: '#1F2937', // gray-800
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    minHeight: 44,
  },
});

// SECONDARY: Visible background
<Pressable style={styles.secondaryButton}>
  <Text style={{ color: '#1F2937' }}>Cancel</Text>
</Pressable>

const styles = StyleSheet.create({
  secondaryButton: {
    backgroundColor: '#F3F4F6', // gray-100
    minHeight: 44,
  },
});

// GHOST: MUST have visible border
<Pressable style={styles.ghostButton}>
  <Text style={{ color: '#374151' }}>Skip</Text>
</Pressable>

const styles = StyleSheet.create({
  ghostButton: {
    borderWidth: 1,
    borderColor: '#D1D5DB', // gray-300
    minHeight: 44,
  },
});

// NEVER CREATE invisible buttons:
// ✗ backgroundColor: 'transparent' without border
// ✗ Text color matching background
```

### 4. Accessibility Labels (REQUIRED)
```tsx
// EVERY interactive element needs accessibility props

// Buttons
<Pressable
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Submit form"
  accessibilityHint="Double tap to submit your information"
>
  <Text>Submit</Text>
</Pressable>

// Icon buttons (NO visible text = MUST have label)
<Pressable
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Close menu"
>
  <CloseIcon />
</Pressable>

// Images
<Image
  accessible={true}
  accessibilityRole="image"
  accessibilityLabel="User profile photo"
  source={...}
/>
```

### 5. Focus/Selection States
```tsx
// EVERY Pressable needs visible pressed state
<Pressable
  style={({ pressed }) => [
    styles.button,
    pressed && styles.buttonPressed,
  ]}
>
  {children}
</Pressable>

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#1F2937',
  },
  buttonPressed: {
    opacity: 0.7,
    // OR
    backgroundColor: '#374151',
  },
});
```

---

## Core Philosophy

**Mobile UI is about touch, speed, and focus.** No hover states, smaller screens, thumb-friendly targets. Design for one-handed use and interruption recovery.

## Platform Differences

### iOS vs Android
```typescript
import { Platform } from 'react-native';

// Platform-specific values
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 8,
    },
    android: {
      elevation: 4,
    },
  }),

  // iOS uses SF Pro, Android uses Roboto
  text: {
    fontFamily: Platform.OS === 'ios' ? 'System' : 'Roboto',
  },
});
```

### Design Language
```
iOS (Human Interface Guidelines)
─────────────────────────────────
- Flat design with subtle depth
- SF Symbols for icons
- Large titles (34pt)
- Rounded corners (10-14pt)
- Blue as default tint

Android (Material Design 3)
─────────────────────────────────
- Material You dynamic color
- Outlined/filled icons
- Medium titles (22pt)
- Rounded corners (12-28pt)
- Primary color from theme
```

## Spacing System

### 4px Base Grid
```typescript
// React Native spacing - consistent scale
const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
} as const;

// Usage
const styles = StyleSheet.create({
  container: {
    padding: spacing.md,
    gap: spacing.sm,
  },
});
```

### Safe Areas
```tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const Screen = ({ children }) => {
  const insets = useSafeAreaInsets();

  return (
    <View style={{
      flex: 1,
      paddingTop: insets.top,
      paddingBottom: insets.bottom,
      paddingLeft: Math.max(insets.left, 16),
      paddingRight: Math.max(insets.right, 16),
    }}>
      {children}
    </View>
  );
};
```

## Typography

### Type Scale
```typescript
const typography = {
  // Large titles (iOS style)
  largeTitle: {
    fontSize: 34,
    fontWeight: '700' as const,
    letterSpacing: 0.37,
  },

  // Section headers
  title: {
    fontSize: 22,
    fontWeight: '700' as const,
    letterSpacing: 0.35,
  },

  // Card titles
  headline: {
    fontSize: 17,
    fontWeight: '600' as const,
    letterSpacing: -0.41,
  },

  // Body text
  body: {
    fontSize: 17,
    fontWeight: '400' as const,
    letterSpacing: -0.41,
    lineHeight: 22,
  },

  // Secondary text
  callout: {
    fontSize: 16,
    fontWeight: '400' as const,
    letterSpacing: -0.32,
  },

  // Small labels
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
};
```

## Color System

### Semantic Colors
```typescript
// Use semantic names, not literal colors
const colors = {
  // Backgrounds
  background: '#FFFFFF',
  backgroundSecondary: '#F2F2F7',
  backgroundTertiary: '#FFFFFF',

  // Surfaces
  surface: '#FFFFFF',
  surfaceElevated: '#FFFFFF',

  // Text
  label: '#000000',
  labelSecondary: '#3C3C43', // 60% opacity
  labelTertiary: '#3C3C43',  // 30% opacity

  // Actions
  primary: '#007AFF',
  destructive: '#FF3B30',
  success: '#34C759',
  warning: '#FF9500',

  // Separators
  separator: '#3C3C43', // 29% opacity
  opaqueSeparator: '#C6C6C8',
};

// Dark mode variants
const darkColors = {
  background: '#000000',
  backgroundSecondary: '#1C1C1E',
  label: '#FFFFFF',
  labelSecondary: '#EBEBF5', // 60% opacity
  separator: '#545458',
};
```

### Dynamic Colors (React Native)
```tsx
import { useColorScheme } from 'react-native';

const useColors = () => {
  const scheme = useColorScheme();
  return scheme === 'dark' ? darkColors : colors;
};

// Usage
const MyComponent = () => {
  const colors = useColors();
  return (
    <View style={{ backgroundColor: colors.background }}>
      <Text style={{ color: colors.label }}>Hello</Text>
    </View>
  );
};
```

## Touch Targets

### Minimum Sizes
```typescript
// CRITICAL: Minimum 44pt touch targets
const touchable = {
  minHeight: 44,
  minWidth: 44,
};

// Button with proper sizing
const styles = StyleSheet.create({
  button: {
    minHeight: 44,
    paddingHorizontal: 16,
    paddingVertical: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Icon button (square)
  iconButton: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // List row
  listRow: {
    minHeight: 44,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
});
```

### Touch Feedback
```tsx
import { Pressable } from 'react-native';

// iOS-style opacity feedback
const Button = ({ children, onPress }) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [
      styles.button,
      pressed && { opacity: 0.7 },
    ]}
  >
    {children}
  </Pressable>
);

// Android-style ripple
const AndroidButton = ({ children, onPress }) => (
  <Pressable
    onPress={onPress}
    android_ripple={{
      color: 'rgba(0, 0, 0, 0.1)',
      borderless: false,
    }}
    style={styles.button}
  >
    {children}
  </Pressable>
);
```

## Component Patterns

### Cards
```tsx
const Card = ({ children, style }) => (
  <View style={[styles.card, style]}>
    {children}
  </View>
);

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.08,
        shadowRadius: 8,
      },
      android: {
        elevation: 2,
      },
    }),
  },
});
```

### Buttons
```tsx
// Primary button
const PrimaryButton = ({ title, onPress, disabled }) => (
  <Pressable
    onPress={onPress}
    disabled={disabled}
    style={({ pressed }) => [
      styles.primaryButton,
      pressed && styles.primaryButtonPressed,
      disabled && styles.buttonDisabled,
    ]}
  >
    <Text style={styles.primaryButtonText}>{title}</Text>
  </Pressable>
);

const styles = StyleSheet.create({
  primaryButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 24,
    alignItems: 'center',
  },
  primaryButtonPressed: {
    backgroundColor: '#0056B3',
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: '600',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
});

// Secondary button
const SecondaryButton = ({ title, onPress }) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [
      styles.secondaryButton,
      pressed && { opacity: 0.7 },
    ]}
  >
    <Text style={styles.secondaryButtonText}>{title}</Text>
  </Pressable>
);
```

### Input Fields
```tsx
const TextField = ({ label, value, onChangeText, error }) => {
  const [focused, setFocused] = useState(false);

  return (
    <View style={styles.textFieldContainer}>
      {label && (
        <Text style={styles.textFieldLabel}>{label}</Text>
      )}
      <TextInput
        value={value}
        onChangeText={onChangeText}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={[
          styles.textField,
          focused && styles.textFieldFocused,
          error && styles.textFieldError,
        ]}
        placeholderTextColor="#8E8E93"
      />
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  textFieldContainer: {
    gap: 8,
  },
  textFieldLabel: {
    fontSize: 15,
    fontWeight: '500',
    color: '#3C3C43',
  },
  textField: {
    backgroundColor: '#F2F2F7',
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 17,
    color: '#000000',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  textFieldFocused: {
    borderColor: '#007AFF',
    backgroundColor: '#FFFFFF',
  },
  textFieldError: {
    borderColor: '#FF3B30',
  },
  errorText: {
    fontSize: 13,
    color: '#FF3B30',
  },
});
```

### Lists
```tsx
// Grouped list (iOS Settings style)
const GroupedList = ({ sections }) => (
  <ScrollView style={styles.groupedList}>
    {sections.map((section, i) => (
      <View key={i} style={styles.section}>
        {section.title && (
          <Text style={styles.sectionHeader}>{section.title}</Text>
        )}
        <View style={styles.sectionContent}>
          {section.items.map((item, j) => (
            <React.Fragment key={j}>
              {j > 0 && <View style={styles.separator} />}
              <Pressable
                style={({ pressed }) => [
                  styles.listRow,
                  pressed && { backgroundColor: '#E5E5EA' },
                ]}
                onPress={item.onPress}
              >
                <Text style={styles.listRowText}>{item.title}</Text>
                <ChevronRight color="#C7C7CC" />
              </Pressable>
            </React.Fragment>
          ))}
        </View>
      </View>
    ))}
  </ScrollView>
);

const styles = StyleSheet.create({
  groupedList: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  section: {
    marginTop: 35,
  },
  sectionHeader: {
    fontSize: 13,
    fontWeight: '400',
    color: '#6D6D72',
    textTransform: 'uppercase',
    marginLeft: 16,
    marginBottom: 8,
  },
  sectionContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    marginHorizontal: 16,
    overflow: 'hidden',
  },
  listRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
    paddingHorizontal: 16,
    minHeight: 44,
  },
  separator: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: '#C6C6C8',
    marginLeft: 16,
  },
});
```

## Navigation Patterns

### Bottom Tab Bar
```tsx
// Proper bottom tab sizing
const tabBarStyle = {
  height: Platform.OS === 'ios' ? 83 : 65, // Account for home indicator
  paddingBottom: Platform.OS === 'ios' ? 34 : 10,
  paddingTop: 10,
  backgroundColor: '#F8F8F8',
  borderTopWidth: StyleSheet.hairlineWidth,
  borderTopColor: '#C6C6C8',
};

// Tab item
const TabItem = ({ icon, label, active }) => (
  <View style={styles.tabItem}>
    <Icon name={icon} color={active ? '#007AFF' : '#8E8E93'} size={24} />
    <Text style={[
      styles.tabLabel,
      { color: active ? '#007AFF' : '#8E8E93' }
    ]}>
      {label}
    </Text>
  </View>
);
```

### Header
```tsx
// Large title header (iOS)
const LargeTitleHeader = ({ title, rightAction }) => {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.header, { paddingTop: insets.top }]}>
      <View style={styles.headerContent}>
        <Text style={styles.largeTitle}>{title}</Text>
        {rightAction}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#F8F8F8',
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#C6C6C8',
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingBottom: 8,
  },
  largeTitle: {
    fontSize: 34,
    fontWeight: '700',
    letterSpacing: 0.37,
  },
});
```

## Animations

### Native Driver Animations
```tsx
import { Animated } from 'react-native';

// Always use native driver when possible
const fadeIn = (value: Animated.Value) => {
  Animated.timing(value, {
    toValue: 1,
    duration: 200,
    useNativeDriver: true, // CRITICAL for performance
  }).start();
};

// Spring for natural feel
const bounce = (value: Animated.Value) => {
  Animated.spring(value, {
    toValue: 1,
    damping: 15,
    stiffness: 150,
    useNativeDriver: true,
  }).start();
};
```

### Reanimated for Complex Animations
```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

const AnimatedCard = ({ children }) => {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const onPressIn = () => {
    scale.value = withSpring(0.95);
  };

  const onPressOut = () => {
    scale.value = withSpring(1);
  };

  return (
    <Pressable onPressIn={onPressIn} onPressOut={onPressOut}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {children}
      </Animated.View>
    </Pressable>
  );
};
```

## Loading States

### Skeleton Loader
```tsx
const SkeletonLoader = ({ width, height, borderRadius = 4 }) => {
  const opacity = useSharedValue(0.3);

  useEffect(() => {
    opacity.value = withRepeat(
      withSequence(
        withTiming(1, { duration: 500 }),
        withTiming(0.3, { duration: 500 })
      ),
      -1,
      false
    );
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return (
    <Animated.View
      style={[
        { width, height, borderRadius, backgroundColor: '#E5E5EA' },
        animatedStyle,
      ]}
    />
  );
};
```

### Activity Indicator
```tsx
import { ActivityIndicator } from 'react-native';

// Use platform-native indicator
<ActivityIndicator size="large" color="#007AFF" />

// Button with loading state
const LoadingButton = ({ loading, title, onPress }) => (
  <Pressable
    onPress={onPress}
    disabled={loading}
    style={styles.button}
  >
    {loading ? (
      <ActivityIndicator color="#FFFFFF" />
    ) : (
      <Text style={styles.buttonText}>{title}</Text>
    )}
  </Pressable>
);
```

## Accessibility

### VoiceOver / TalkBack
```tsx
// Accessible button
<Pressable
  onPress={onPress}
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Submit form"
  accessibilityHint="Double tap to submit your information"
>
  <Text>Submit</Text>
</Pressable>

// Accessible image
<Image
  source={icon}
  accessible={true}
  accessibilityRole="image"
  accessibilityLabel="User profile picture"
/>

// Group related elements
<View
  accessible={true}
  accessibilityRole="summary"
  accessibilityLabel={`${name}, ${role}, ${status}`}
>
  <Text>{name}</Text>
  <Text>{role}</Text>
  <Text>{status}</Text>
</View>
```

### Dynamic Type (iOS)
```tsx
import { PixelRatio } from 'react-native';

// Scale fonts with system settings
const fontScale = PixelRatio.getFontScale();
const scaledFontSize = (size: number) => size * fontScale;

// Or use allowFontScaling
<Text allowFontScaling={true} style={{ fontSize: 17 }}>
  This text scales with system settings
</Text>
```

## Anti-Patterns

### Never Do
```
✗ Touch targets smaller than 44pt
✗ Text smaller than 12pt
✗ Hover states (no hover on mobile)
✗ Fixed heights that break with large text
✗ Ignoring safe areas
✗ Heavy shadows on Android (use elevation)
✗ White text on light backgrounds without checking contrast
✗ Non-native animations (JS-driven transforms)
✗ Ignoring platform conventions (iOS vs Android)
✗ Inline styles everywhere (use StyleSheet.create)
```

### Common Mistakes
```tsx
// ✗ Hardcoded dimensions that break accessibility
style={{ height: 40 }}  // Text might be larger

// ✓ Minimum height with padding
style={{ minHeight: 44, paddingVertical: 12 }}

// ✗ Shadow on Android
shadowColor: '#000'  // Won't work

// ✓ Platform-specific
...Platform.select({
  ios: { shadowColor: '#000', ... },
  android: { elevation: 4 },
})

// ✗ Fixed status bar height
paddingTop: 44

// ✓ Use safe area
paddingTop: insets.top
```

## Quick Reference

### Mobile Defaults
```
Touch targets: 44pt minimum
Font sizes: 12pt min, 17pt body, 34pt large title
Border radius: 10-14pt (iOS), 12-28pt (Android)
Spacing: 4/8/16/24/32 grid
Animations: 200-300ms, native driver
Shadow: iOS shadowOpacity 0.08-0.15, Android elevation 2-8
```

### Premium Feel Checklist
```
□ All touch targets 44pt+
□ Consistent spacing (4pt grid)
□ Platform-appropriate styling
□ Safe area handling
□ Native animations (60fps)
□ Proper loading states
□ Dark mode support
□ Accessibility labels
□ Haptic feedback on actions
□ Pull-to-refresh where appropriate
```
