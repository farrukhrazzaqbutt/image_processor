
# Django Project: Image Processor

This Django project allows users to upload CSV files containing image data, store processed images in the database, and retrieve those images with optional dynamic color mapping through an API. The project is built with two main Django apps:

- **image_processor**: The primary Django app.
- **images**: Handles image processing, storage, and API endpoints.

---

## Features

1. **Upload CSV File**:
   - Upload a CSV file containing image data (e.g., pixel values and depth).
   - Process and resize images, then save them to the database.

2. **Retrieve Images**:
   - Fetch images from the database by depth or depth range.
   - Dynamically apply color maps to images during retrieval.

3. **Database**:
   - Uses `SQLite3` (`db.sqlite3`) to store image metadata and binary data.

4. **Docker and Kubernetes Support**:
   - Deployable using Docker and Docker Compose.
   - Kubernetes configurations provided for scalable deployments.

---

## Project Structure

```
project_root/
├── image_processor/            # Main app
├── images/                     # Image handling app
│   ├── views.py                # API endpoints for image processing
│   ├── utils.py                # Helper functions for CSV processing
│   ├── urls.py                 # URL routes for the images app
├── db.sqlite3                  # SQLite database file
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── k8s-deployment.yaml         # Kubernetes configuration
├── requirements.txt            # Python dependencies
├── manage.py                   # Django entry point
├── README.md                   # Project documentation
```

---

## Endpoints

### **1. Upload CSV**
**URL**: `/upload-csv/`

**Method**: `POST`

Uploads a CSV file containing image data. The file should have:
- `depth`: Float representing image depth.
- `col1` to `col200`: Pixel intensity values (0-255).

**Response**:
- `200 OK`: Successfully processed and stored images.
- `500 Internal Server Error`: On failure.

### **2. Retrieve Images by Depth Range**
**URL**: `/get-images/<depth_min>/<depth_max>/`

**Method**: `GET`

Fetches images within the specified depth range. Dynamically applies a color map during retrieval.

**Query Parameters**:
- `colormap` (optional): Specify a Matplotlib colormap (e.g., `viridis`, `plasma`).

**Response**:
- `200 OK`: JSON containing Base64-encoded images and their depths.
- `404 Not Found`: No images found in the specified range.

---

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd project_root
```

### **2. Install Dependencies**
#### Using Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **3. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Start the Development Server**
```bash
python manage.py runserver
```

Access the project at `http://127.0.0.1:8000/`.

---

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t django_image_processor .
   ```

2. Start the container:
   ```bash
   docker-compose up -d
   ```

Access the application at `http://localhost:8000/`.

---

## Kubernetes Deployment

1. Apply the Kubernetes configurations:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

2. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

3. Access the application via the LoadBalancer URL.

---

## Environment Variables

Set the following environment variables in a `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
```

---

## Dependencies

- **Django**: Web framework
- **Gunicorn**: WSGI server for deployment
- **Pillow**: Image processing
- **Matplotlib**: Color mapping

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License.
