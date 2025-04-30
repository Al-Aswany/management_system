# Management System

This repository contains a comprehensive Company Management System application built using the Frappe Framework.

## Approach and Implementation Details

The system is developed as a custom Frappe application, developing a Company Management System that encompasses various features for managing companies, departments, employees, and projects.

### Key Modules and Features

The application is structured around several key DocTypes representing core business entities:

*   **MS Company:** Manages company information. Includes details like company name and tracks aggregated data such as the number of departments, employees, and projects associated with the company.
*   **MS Department:** Manages department information within a specific company. Tracks department name, associated company, and aggregates data like the number of employees and projects within the department.
*   **MS Employee:** Manages employee records. Includes personal details (name, email, mobile, address), employment information (company, department, title, hire date), and tracks assigned projects.
*   **MS Project:** Manages project details. Includes project name, associated company and department, description, start/end dates, and allows assignment of multiple employees to the project via the `Employee Project` child table.
*   **Performance Review:** Manages employee performance reviews.
*   **User Account:** Manages user accounts linked to employees.
*   **Employee Project:** A child DocType linking Employees to Projects, enabling many-to-many relationships.

### Implementation Considerations

*   **Modularity:** The application is designed with distinct DocTypes for each major entity, promoting modularity and ease of maintenance.
*   **Data Aggregation:** Several DocTypes include calculated fields (e.g., `number_of_employees` in MS Company) to provide quick summaries. These are likely updated via Frappe's hooks or custom scripts (further investigation needed for exact mechanism).
*   **API Access:** The system exposes a RESTful API for interacting with the core DocTypes (Company, Department, Employee, Project). These APIs support fetching lists, retrieving individual records, creating, updating, and deleting records.

## Setup and Running the Application

Follow these instructions to set up and run the Management System application locally.


### Installation Steps

1.  **Navigate to your Frappe Bench directory:**
    ```bash
    cd [your-bench-directory]
    ```

2.  **Get the app from the repository:**
    ```bash
    bench get-app https://github.com/Al-Aswany/management_system.git
    ```
    This command clones the repository into your bench's `apps` folder.

3.  **Create a new site (if you don't have one already):**
    ```bash
    bench new-site [your-site-name]
    ```
    Replace `[your-site-name]` with the desired name for your site (e.g., `management.local`). You will be prompted for the MySQL root password and to set an administrator password for the new site.

4.  **Install the app on your site:**
    ```bash
    bench --site [your-site-name] install-app management_system
    ```
    This installs the `management_system` app, including its DocTypes and configurations, into the specified site.

5.  **Run database migrations (optional but recommended):**
    ```bash
    bench --site [your-site-name] migrate
    ```
    This ensures your site's database schema is up-to-date with the app's definitions.

### Running the Application

1.  **Start the Frappe Bench development server:**
    ```bash
    cd [your-bench-directory]
    bench start
    ```
    This command starts the necessary services (web server, background workers, etc.).

2.  **Access the application:**
    Open your web browser and navigate to `http://[your-site-name]:8000` (or the appropriate URL/port for your setup).
    Log in using the administrator credentials you set during site creation or other user credentials.


### Assumptions and Considerations

*   **Calculated Fields:** The mechanism for updating aggregated fields (like `number_of_employees`) is assumed to be handled either by Frappe's standard calculations or potentially requires custom scripts/hooks not fully detailed in the examined files.

## API Documentation

The application provides RESTful API endpoints for interacting with the core DocTypes. Access these endpoints through your Frappe site URL.

**Base URL:** `http://[your-site-name]:8000/api/method/management_system.api.[module].[function_name]`

**Authentication:** All API calls require authentication (e.g., using API keys and secrets generated in Frappe).

### Company API (`management_system.api.company`)

*   **`get_companies`**
    *   **Method:** GET
    *   **Description:** Retrieves a list of all companies or a specific company.
    *   **Endpoint:** `/api/method/management_system.api.company.get_companies`
    *   **Parameters (Query String):**
        *   `company` (optional): The name (ID) of the specific company to retrieve.

### Department API (`management_system.api.department`)

*   **`get_departments`**
    *   **Method:** GET
    *   **Description:** Retrieves a list of all departments or a specific department.
    *   **Endpoint:** `/api/method/management_system.api.department.get_departments`
    *   **Parameters (Query String):**
        *   `department` (optional): The name (ID) of the specific department to retrieve.
    *   **Success Response (List/Single):** Similar structure to `get_companies`, containing department details (`name`, `department_name`, `company`, `number_of_employees`, `number_of_projects`).

### Employee API (`management_system.api.employee`)

*   **`get_employees`**
    *   **Method:** GET
    *   **Description:** Retrieves a list of all employees or a specific employee.
    *   **Endpoint:** `/api/method/management_system.api.employee.get_employees`
    *   **Parameters (Query String):**
        *   `employee` (optional): The name (ID) of the specific employee to retrieve.
    *   **Success Response (List/Single):** Contains employee details (`name`, `employee_name`, `email_address`, `mobile_number`, `address`, `company`, `department`, `title`, `hired`, `hired_on`, `days_employed`, `number_of_assigned_projects`).
*   **`create_employee`**
    *   **Method:** POST
    *   **Description:** Creates a new employee record.
    *   **Endpoint:** `/api/method/management_system.api.employee.create_employee`
    *   **Request Body (JSON):** Object containing employee fields (e.g., `{"employee_name": "John Doe", "email_address": "john.doe@example.com", ...}`).
    *   **Success Response:**
        ```json
        {
          "status": "success",
          "message": "Employee created successfully",
          "data": { ... newly created employee data ... }
        }
        ```
*   **`update_employee`**
    *   **Method:** POST (or PUT/PATCH, depending on Frappe conventions/client usage)
    *   **Description:** Updates an existing employee record.
    *   **Endpoint:** `/api/method/management_system.api.employee.update_employee`
    *   **Request Body (JSON):** Object containing employee fields to update, including the `name` (ID) of the employee (e.g., `{"name": "EMP-0001", "title": "Senior Developer", ...}`).
    *   **Success Response:**
        ```json
        {
          "status": "success",
          "message": "Employee updated successfully",
          "data": { ... updated employee data ... }
        }
        ```
*   **`delete_employee`**
    *   **Method:** POST (or DELETE, depending on Frappe conventions/client usage)
    *   **Description:** Deletes an employee record.
    *   **Endpoint:** `/api/method/management_system.api.employee.delete_employee`
    *   **Request Body (JSON):** Object containing the `name` (ID) of the employee to delete (e.g., `{"name": "EMP-0001"}`).
    *   **Success Response:**
        ```json
        {
          "status": "success",
          "message": "Employee deleted successfully"
        }
        ```

### Project API (`management_system.api.project`)

*   **`get_projects`**
    *   **Method:** GET
    *   **Description:** Retrieves a list of all projects or a specific project, including assigned employees.
    *   **Endpoint:** `/api/method/management_system.api.project.get_projects`
    *   **Parameters (Query String):**
        *   `project` (optional): The name (ID) of the specific project to retrieve.
    *   **Success Response (List/Single):** Contains project details (`name`, `project_name`, `company`, `department`, `description`, `start_date`, `end_date`) and a list of `assigned_employees` (containing `employee` ID).
*   **`create_project`**
    *   **Method:** POST
    *   **Description:** Creates a new project record, optionally assigning employees.
    *   **Endpoint:** `/api/method/management_system.api.project.create_project`
    *   **Request Body (JSON):** Object containing project fields and an optional `assigned_employees` array (e.g., `{"project_name": "New Initiative", ..., "assigned_employees": [{"employee": "EMP-0001"}, {"employee": "EMP-0002"}]}`).
    *   **Success Response:** Similar structure to `create_employee`, returning created project data.
*   **`update_project`**
    *   **Method:** POST (or PUT/PATCH)
    *   **Description:** Updates an existing project record, including assigned employees.
    *   **Endpoint:** `/api/method/management_system.api.project.update_project`
    *   **Request Body (JSON):** Object containing project fields to update, including the `name` (ID) and optionally the `assigned_employees` array (existing assignments are typically cleared and replaced).
    *   **Success Response:** Similar structure to `update_employee`, returning updated project data.
*   **`delete_project`**
    *   **Method:** POST (or DELETE)
    *   **Description:** Deletes a project record.
    *   **Endpoint:** `/api/method/management_system.api.project.delete_project`
    *   **Request Body (JSON):** Object containing the `name` (ID) of the project to delete.
    *   **Success Response:** Similar structure to `delete_employee`.



#### License

MIT
