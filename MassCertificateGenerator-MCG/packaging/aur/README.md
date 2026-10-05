# Publishing Mass Certificate Generator to Arch User Repository (AUR)

This directory contains pre-configured, tested packaging scripts for releasing **Mass Certificate Generator** to the Arch User Repository (AUR).

Two packages are provided:
1. **`mass-certificate-generator` (Recommended native package)**:
   - Architecture: `any` (pure Python using native Arch libraries).
   - Dependencies: `pyside6`, `python-pymupdf`, `python-pandas`, `python-openpyxl`.
   - Installed size: **~1.5 MB** (uses system libraries).
2. **`mass-certificate-generator-bin` (Standalone binary package)**:
   - Architecture: `x86_64`.
   - Downloads the pre-compiled GitHub release tarball.
   - Installs without requiring system Python/Qt dependencies.

---

## Step-by-Step Instructions

### Step 1: Register an AUR Account & Configure SSH Key

1. Go to [https://aur.archlinux.org](https://aur.archlinux.org) and register an account.
2. In your AUR account settings (**My Account**), upload your public SSH key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # If you don't have an SSH key yet, generate one:
   # ssh-keygen -t ed25519 -C "kazirifatmorshed@gmail.com"
   ```
3. Test your SSH connection:
   ```bash
   ssh -T aur@aur.archlinux.org
   ```

---

### Step 2: Choose Your Package Name & Clone from AUR

For the native source package (`mass-certificate-generator`):
```bash
git clone ssh://aur@aur.archlinux.org/mass-certificate-generator.git /tmp/aur-mcg
```

*(Note: If the package is brand new, git will inform you that you have cloned an empty repository. That is normal!)*

---

### Step 3: Copy Packaging Files & Generate `.SRCINFO`

```bash
# Copy PKGBUILD and .desktop file into your cloned AUR repository
cp packaging/aur/mass-certificate-generator/PKGBUILD /tmp/aur-mcg/
cp packaging/aur/mass-certificate-generator/mass-certificate-generator.desktop /tmp/aur-mcg/

cd /tmp/aur-mcg

# Generate .SRCINFO (MANDATORY for AUR)
makepkg --printsrcinfo > .SRCINFO
```

---

### Step 4: Test Build Locally

Always test the build on your local machine before pushing:
```bash
makepkg -si
```
Verify that `mass-certificate-generator` launches and functions properly.

---

### Step 5: Commit and Push to the AUR

```bash
git add PKGBUILD .SRCINFO mass-certificate-generator.desktop
git commit -m "Initial release of mass-certificate-generator v1.1.0"
git push origin master
```

---

### Step 6: Verify on the AUR

Your package is now live! Arch and Manjaro users can immediately install it using any AUR helper:
```bash
yay -S mass-certificate-generator
# or
paru -S mass-certificate-generator
# or via Pamac GUI on Manjaro
```

---

## For the Binary Release (`mass-certificate-generator-bin`)

If you want to release the `-bin` variant:
1. First, create a GitHub release `v1.1.0` on GitHub and upload `MassCertificateGenerator-v1.1.0-linux-x86_64.tar.gz`.
2. Compute the SHA256 checksum:
   ```bash
   sha256sum dist/MassCertificateGenerator-v1.1.0-linux-x86_64.tar.gz
   ```
3. Update `sha256sums=('...')` in `packaging/aur/mass-certificate-generator-bin/PKGBUILD`.
4. Clone `ssh://aur@aur.archlinux.org/mass-certificate-generator-bin.git`.
5. Copy `PKGBUILD`, run `makepkg --printsrcinfo > .SRCINFO`, commit, and push.
