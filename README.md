# Cranecloud CLI Client

Cranecloud CLI client is a command line tool for interacting with Cranecloud.

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
   cranecloud projects create --name "ProjectName"
   ```

3. **Delete Project:** Delete a project by ID or name.

   ```bash
   cranecloud projects delete --id <project_id>
   ```

4. **Project Details:** View detailed information about a project.

   ```bash
   cranecloud projects info --id <project_id>
   ```

### App Commands

1. **Deploy App:** Initiate a app to a specific environment.

   ```bash
   cranecloud apps --project-id <project_id> --environment <env_name>
   ```

2. **List Apps:** Show apps within a project.

   ```bash
   cranecloud apps list --project-id <project_id>
   ```

3. **Rollback App:** Roll back to a previous app version.

   ```bash
   cranecloud apps rollback --project-id <project_id> --app-id <app_id>
   ```

4. **App Details:** View detailed information about a specific app.

   ```bash
   cranecloud apps info --project-id <project_id> --app-id <app_id>
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
