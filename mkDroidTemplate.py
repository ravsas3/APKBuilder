import os
import subprocess

# --- CONFIGURATION ---
PROJECT=os.environ.get("PROJECT")
PROJECT_NAME = PROJECT+"App"
PACKAGE_NAME = "com.example."+PROJECT.lower()
SDK_PATH = os.environ.get("ANDROID_HOME") # Ensure ANDROID_HOME is set

# Directory Structure
DIRS = [
    f"{PROJECT_NAME}/app/src/main/java/{PACKAGE_NAME.replace('.', '/')}",
    f"{PROJECT_NAME}/app/src/main/res/layout",
    f"{PROJECT_NAME}/app/src/main/res/values",
    f"{PROJECT_NAME}/gradle/wrapper"
]

# Basic AndroidManifest.xml content
MANIFEST = f'''<?xml version="1.0" encoding="utf-8"?>
<!--<manifest xmlns:android="schemas.microsoft.com" package="{PACKAGE_NAME}">-->
<!--<manifest xmlns:android="schemas.microsoft.com">-->
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:label="{PROJECT_NAME}">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''

# Simple MainActivity.java content
JAVA_CODE = f'''package {PACKAGE_NAME};
import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        tv.setText("Hello from Python Script!");
        setContentView(tv);
    }}
}}'''

def create_structure():
    print(f"[*] Creating project structure for {PROJECT_NAME}...")
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
    
    # Write files
    with open(f"{PROJECT_NAME}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(MANIFEST)
    with open(f"{PROJECT_NAME}/app/src/main/java/{PACKAGE_NAME.replace('.', '/')}/MainActivity.java", "w") as f:
        f.write(JAVA_CODE)

def build_app():
    print("[*] Starting build process...")
    # NOTE: In a real scenario, you would copy 'gradlew' and 'build.gradle' templates here.
    # For a quick start, we use the local gradle wrapper if available.
    try:
        os.chdir(PROJECT_NAME)
        # Standard Gradle build command
        #subprocess.run(["./gradlew", "assembleDebug"], check=True)
        subprocess.run(["gradlew.bat", "clean", "assembleDebug"], check=True)
        print("[+] Build Successful! APK located in app/build/outputs/apk/debug/")
    except Exception as e:
        print(f"[-] Build failed: {e}")

import os

# 1. Root build.gradle (Project-level)
ROOT_GRADLE = '''buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.13.2"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
'''

# 2. settings.gradle
SETTINGS_GRADLE = f"include ':app'\nrootProject.name = '{PROJECT_NAME}'"

# 3. app/build.gradle (Module-level)
# Note: AGP 8.0+ requires 'namespace' and doesn't use buildToolsVersion by default
APP_GRADLE = f'''apply plugin: 'com.android.application'

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 34

    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
}}
'''

GRADLE_W = '''@echo off
set DIR=%~dp0
set APP_HOME=%DIR%

if defined JAVA_HOME (
  set JAVA_EXE=%JAVA_HOME\\bin\java.exe
) else (
  set JAVA_EXE=java.exe
)

"%JAVA_EXE%" -Xmx64m -Xms64m -classpath "%APP_HOME%\gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*'''

def setup_project():
    print(f"[*] Creating project: {PROJECT_NAME}")
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
    
    # Write Gradle Configuration Files
    with open(f"{PROJECT_NAME}/build.gradle", "w") as f:
        f.write(ROOT_GRADLE)
    with open(f"{PROJECT_NAME}/settings.gradle", "w") as f:
        f.write(SETTINGS_GRADLE)
    with open(f"{PROJECT_NAME}/app/build.gradle", "w") as f:
        f.write(APP_GRADLE)
    with open(f"{PROJECT_NAME}/gradlew.bat", "w") as f:
        f.write(GRADLE_W)

    print("[+] Configuration files generated successfully.")
    

if __name__ == "__main__":
    if not SDK_PATH:
        print("Error: ANDROID_HOME environment variable not set.")
    else:
        create_structure()
        setup_project()
        print("Project template created. you can write your code now!!")
        print("[!] Note: You must place a valid build.gradle and gradlew files in the root before building.")
