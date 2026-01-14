import os
import subprocess
import sys

# --- CONFIGURATION ---
PROJECT_NAME = "CameraApp"
SDK_PATH = os.environ.get("ANDROID_HOME") # Ensure ANDROID_HOME is set

def build_app():
    print("[*] Starting build process...")
    # NOTE: In a real scenario, you would copy 'gradlew' and 'build.gradle' templates here.
    # For a quick start, we use the local gradle wrapper if available.
    try:
        os.chdir(PROJECT_NAME)
        # Standard Gradle build command
        #subprocess.run(["./gradlew", "assembleDebug"], check=True)
        #subprocess.run(["gradlew.bat", "clean", "build"], check=True)
        #print("[+] Build Successful! APK located in app/build/outputs/apk/debug/")
        subprocess.run(["gradlew.bat", "clean", "assembleDebug"], check=True)
        print("[+] Build Successful! APK located in app/build/outputs/apk/debug/")
    except Exception as e:
        print(f"[-] Build failed: {e}")
        sys.exit(1)   # non-zero = error

if __name__ == "__main__":
    if not SDK_PATH:
        print("Error: ANDROID_HOME environment variable not set.")
    else:
        print("[!] Note: You must place a valid build.gradle and gradlew files in the root before building.")
        build_app() # Uncomment once build.gradle is added
        #move file to PROJECT_NAME.apk
        APKNAME=PROJECT_NAME+".apk"
