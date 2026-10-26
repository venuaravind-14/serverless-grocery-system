# serverless-inventory-management-system

This project demonstrates how to build a clean and scalable full-stack **inventory management system** using **pure AWS serverless components**. With React on the frontend and Terraform on the backend, it is cloud-native and production-ready.

## 📁 Cloud Architecture & Services

This full-stack system leverages **6 AWS Cloud Services** (exceeding the 4-service minimum requirement):

1. **Amazon DynamoDB**: NoSQL database for fast, flexible, and scalable storage of inventory items with on-demand capacity (`PAY_PER_REQUEST`).
2. **AWS Lambda**: Serverless Python compute services handling CRUD business logic (`create_item`, `get_items`, `update_item`, `delete_item`).
3. **Amazon API Gateway (HTTP API v2)**: Managed HTTP gateway providing fast, low-latency RESTful routing, CORS handling, and proxy integrations.
4. **Amazon S3**: High-availability cloud object storage configured for static website hosting to serve the React Single-Page Application (SPA) to users worldwide.
5. **AWS IAM (Identity & Access Management)**: Enforces least-privilege role-based access control, allowing Lambda functions to interact securely with DynamoDB and CloudWatch.
6. **Amazon CloudWatch**: Centralized cloud logging, monitoring, and debugging for Lambda executions and API requests.

---

## 🔧 Tech Stack

- **Frontend**: React.js (calls API Gateway HTTP API endpoints)
- **Backend**: AWS Lambda (Python 3.11) + Amazon API Gateway HTTP API v2
- **Database**: Amazon DynamoDB
- **Hosting**: Amazon S3 Static Website Hosting
- **Security & Access**: AWS IAM
- **Observability**: Amazon CloudWatch
- **Infrastructure as Code (IaC)**: Terraform

---

## 🚀 Step-by-Step AWS Deployment Guide

### Prerequisites
1. **AWS CLI** installed and configured (`aws configure` with valid Access Key, Secret Key, and default Region e.g. `us-east-1`).
2. **Terraform** (v1.5+) installed.
3. **Node.js** (v18+) and **npm** installed.
4. **Python** (v3.10+) installed.

---

### Step 1: Deploy AWS Infrastructure with Terraform

1. Open your terminal and navigate to the `backend` directory (where `main.tf` is located):
   ```bash
   cd backend
   ```

2. Initialize Terraform (downloads AWS and Archive providers and sets up modules):
   ```bash
   terraform init
   ```

3. Review the execution plan:
   ```bash
   terraform plan
   ```

4. Apply the configuration to provision all AWS resources:
   ```bash
   terraform apply --auto-approve
   ```

5. **Note the Terraform Outputs**:
   After the deployment finishes, Terraform outputs:
   - `api_gateway_url`: e.g. `https://xyz123.execute-api.us-east-1.amazonaws.com`
   - `frontend_bucket_name`: e.g. `inv-mgmt-frontend-20261023...`
   - `frontend_website_url`: e.g. `http://inv-mgmt-frontend-20261023.s3-website-us-east-1.amazonaws.com`

---

### Step 2: Configure the Frontend Environment

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend/inventory-management-system
   ```

2. Open or create the `.env` file and set `REACT_APP_API_URL` to your Terraform `api_gateway_url` output:
   ```env
   REACT_APP_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com
   ```
   *(Ensure there is no trailing slash at the end of the URL)*

---

### Step 3: Test Frontend Locally (Optional)

1. Install frontend dependencies:
   ```bash
   npm install
   ```

2. Start the local development server:
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000` and communicate directly with your live AWS backend!

---

### Step 4: Deploy Frontend to Amazon S3 (Cloud Deployment)

1. Build the production bundle with optimized static files:
   ```bash
   npm run build
   ```

2. Deploy the static assets to the S3 bucket created by Terraform:
   ```bash
   aws s3 sync build/ s3://<YOUR_FRONTEND_BUCKET_NAME> --delete
   ```
   *(Replace `<YOUR_FRONTEND_BUCKET_NAME>` with the `frontend_bucket_name` output from Terraform)*

3. Open your browser and navigate to the `frontend_website_url` output from Terraform:
   ```
   http://<YOUR_FRONTEND_BUCKET_NAME>.s3-website-us-east-1.amazonaws.com
   ```

Your full-stack Inventory Management System is now **100% running in the AWS Cloud**!

---

### Step 5: Clean Up / Destroy Resources

When you are done testing and want to avoid unexpected AWS charges, destroy all provisioned infrastructure:

1. Empty the frontend S3 bucket:
   ```bash
   aws s3 rm s3://<YOUR_FRONTEND_BUCKET_NAME> --recursive
   ```

2. Destroy Terraform resources:
   ```bash
   cd ../../backend
   terraform destroy --auto-approve
   ```
