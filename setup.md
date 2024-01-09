### Setup

1. **Create** and activate a virtual environment

   ```bash
   python3 -m venv venv
   ```

2. **Install:** Run the Cranecloud CLI client setup.

   ```bash
   pip install --editable .
   ```

3. Add `API_BASE_URL` that points to cc backend to your `.env` file

   ```bash
   export API_BASE_URL=""