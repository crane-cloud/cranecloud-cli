# Cranecloud CLI Client

Cranecloud CLI client is a command line tool for interacting with Cranecloud.

## Install via Snap (Linux)

### Install from Snap Store (Recommended)

```bash
sudo snap install cranecloud
```

### Build and Install Locally

You can also build and install a Snap package of the CLI locally.

1. Ensure `snapcraft` is installed. On Ubuntu:

   ```bash
   sudo snap install snapcraft --classic
   ```

2. Build the snap from the project root:

   ```bash
   snapcraft pack
   ```

   This produces a file like `cranecloud_1.0.0_amd64.snap` in the project directory.

3. Install the snap locally:

   ```bash
   sudo snap install --dangerous cranecloud_*.snap
   ```

4. Connect interfaces for network, keyring, and dotfile access (first-time only):

   ```bash
   sudo snap connect cranecloud:password-manager-service
   sudo snap connect cranecloud:dot-crane
   ```

5. Run the CLI:

   ```bash
   cranecloud.cranecloud --help
   ```

   Optionally create a shorter alias:

   ```bash
   sudo snap alias cranecloud.cranecloud cranecloud
   cranecloud --help
   ```

## Basic Commands

### Authentication and Account Management

1. **Login:** Authenticate the user with their credentials.

   ```bash
   cranecloud auth login
   ```

2. **Logout:** Log out the user, clearing the stored credentials.

   ```bash
   cranecloud auth logout
   ```

3. **User Information:** Retrieve information about the logged-in user.

   ```bash
   cranecloud auth user
   ```

### Project Management

1. **List Projects:** Show a list of projects available in the user's account.

   ```bash
   cranecloud projects list
   ```

2. **Create Project:** Create a new project.

   ```bash
   cranecloud projects create ...
   ```

3. **Delete Project:** Delete a project by ID or name.

   ```bash
   cranecloud projects delete --id <project_id>
   ```

4. **Project Details:** View detailed information about a project.

   ```bash
   cranecloud projects info --id <project_id>
   ```

### Configuration Management

1. **List Config:** Show a list of config available for the app.

   ```bash
   cranecloud config get-config
   ```

2. **Set current project to use:** This is projects apps commands will default to.

   ```bash
   cranecloud projects use-project <project_id>
   ```

3. **Set current cluster to use:** This is cluster projects commands will default to.

   ```bash
   cranecloud projects use-project <cluster_id>
   ```

### App Commands

1. **Deploy App:** Initiate a app .

   ```bash
   cranecloud apps deploy
   ```

2. **List Apps:** Show apps within a project.

   ```bash
   cranecloud apps list 
   ```

3. **Update App:** Update app information.

   ```bash
   cranecloud apps update  <app_id>
   ```

4. **App Details:** View detailed information about a specific app.

   ```bash
   cranecloud apps info  <app_id>
   ```

5. **Delete App:** Delete a app by ID or name.

   ```bash
   cranecloud projects delete --id <project_id>
   ```

### Other Useful Commands

1. **Help Information:** Show manual.

   ```bash
   cranecloud help
   ```

2. **Support:** Contact support or report issues.

   ```bash
   cranecloud support
   ```
