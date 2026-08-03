name: Build APK
on: push

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      
      - name: List files
        run: ls -la
      
      - name: Install system dependencies
        run: |
          sudo apt update
          sudo apt install -y python3-pip python3-dev openjdk-17-jdk git autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev gfortran unzip
      
      - name: Install Buildozer
        run: pip install buildozer cython
      
      - name: Accept Android licenses
        run: |
          mkdir -p /home/runner/.buildozer/android/platform/android-sdk/licenses
          echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > /home/runner/.buildozer/android/platform/android-sdk/licenses/android-sdk-license

      - name: Build APK
        run: buildozer android debug
      
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Hprob-APK
          path: bin/*.apk
