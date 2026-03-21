-- PostgreSQL Version of GastroVision v2.0

-- Create Custom Types (Postgres way of doing ENUMS)
CREATE TYPE user_role AS ENUM ('doctor', 'admin', 'researcher');
CREATE TYPE case_status AS ENUM ('pending', 'in_progress', 'completed', 'archived');
CREATE TYPE upload_status_type AS ENUM ('uploading', 'uploaded', 'processing', 'ready');

-- 1. Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    full_name VARCHAR(150),
    role user_role DEFAULT 'doctor',
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Patients Table
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    case_ref VARCHAR(50) UNIQUE NOT NULL,
    patient_name VARCHAR(150) NOT NULL,
    age INT,
    gender VARCHAR(10), -- M, F, Other
    medical_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Cases Table
CREATE TABLE cases (
    case_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    created_by INT NOT NULL REFERENCES users(user_id),
    status case_status DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Videos Table (Updated for Binary Storage)
CREATE TABLE videos (
    video_id SERIAL PRIMARY KEY,
    case_id INT NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    video_filename VARCHAR(255) NOT NULL,
    video_data BYTEA, -- The actual video file
    file_size_mb FLOAT,
    upload_status upload_status_type DEFAULT 'uploaded',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create basic indexes for performance
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_patient_name ON patients(patient_name);
CREATE INDEX idx_case_status ON cases(status);