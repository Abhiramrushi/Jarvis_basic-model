-- Database Schema for Adaptive AI Agent

-- Users table for storing user profiles and preferences
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    preferences JSONB,
    communication_style VARCHAR(50) DEFAULT 'professional',
    response_length VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Interactions table for storing conversation history
CREATE TABLE interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    input_text TEXT,
    response_text TEXT,
    model_used VARCHAR(100),
    confidence_score FLOAT,
    feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Learning data table for storing user learning patterns
CREATE TABLE learning_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    data_type VARCHAR(50), -- 'preference', 'behavior', 'feedback'
    data_content JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vector embeddings table for RAG
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content_type VARCHAR(50), -- 'document', 'conversation', 'preference'
    content TEXT,
    embedding_vector VECTOR(1536), -- Assuming OpenAI embedding dimension
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sessions table for Redis-style session management
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_data JSONB,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_interactions_user_id ON interactions(user_id);
CREATE INDEX idx_interactions_created_at ON interactions(created_at);
CREATE INDEX idx_learning_data_user_id ON learning_data(user_id);
CREATE INDEX idx_embeddings_user_id ON embeddings(user_id);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data insertion
INSERT INTO users (email, name, preferences, communication_style) VALUES
('user1@example.com', 'John Doe', '{"preferred_topics": ["technology", "science"], "satisfaction_score": 4.5}', 'professional'),
('user2@example.com', 'Jane Smith', '{"preferred_topics": ["art", "music"], "satisfaction_score": 4.2}', 'casual');
