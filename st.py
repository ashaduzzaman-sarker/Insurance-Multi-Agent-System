import os
from pathlib import Path

def create_structure():
    # Define the structure: 
    # Keys are directory paths
    # Values are lists of files within those directories
    structure = {
        ".": [
            "pyproject.toml", "README.md", ".env.example", 
            ".gitignore", "Makefile", "docker-compose.yml", "Dockerfile"
        ],
        "docs": [
            "architecture.md", "api_reference.md", "deployment.md", 
            "bangladesh_compliance.md", "user_guide.md"
        ],
        "scripts": [
            "init_db.py", "init_vectorstore.py", "seed_policies.py", "run_tests.sh"
        ],
        "src/bimas": ["__init__.py", "__main__.py"],
        "src/bimas/config": ["__init__.py", "settings.py", "logging_config.py"],
        "src/bimas/core": ["__init__.py", "models.py", "audit.py", "security.py", "exceptions.py"],
        "src/bimas/agents": [
            "__init__.py", "base_agent.py", "extraction_agent.py", 
            "knowledge_agent.py", "risk_logic_agent.py", "fraud_agent.py", 
            "compliance_agent.py", "decision_agent.py"
        ],
        "src/bimas/orchestrator": ["__init__.py", "workflow.py", "executor.py"],
        "src/bimas/rules": ["__init__.py", "engine.py", "bangladesh_rules.py", "validators.py"],
        "src/bimas/rag": ["__init__.py", "vector_store.py", "retriever.py", "embeddings.py"],
        "src/bimas/api": ["__init__.py", "main.py", "dependencies.py", "middleware.py"],
        "src/bimas/api/routes": ["__init__.py", "cases.py", "documents.py", "reviews.py", "audit.py"],
        "src/bimas/api/schemas": ["__init__.py", "case_schemas.py", "document_schemas.py", "review_schemas.py"],
        "src/bimas/ui": ["__init__.py", "dashboard.py"],
        "src/bimas/ui/components": ["__init__.py", "case_viewer.py", "risk_display.py"],
        "src/bimas/db": ["__init__.py", "base.py", "models.py"],
        "src/bimas/db/repositories": ["__init__.py", "case_repository.py", "audit_repository.py"],
        "src/bimas/db/migrations/versions": [],
        "src/bimas/services": ["__init__.py", "case_service.py", "document_service.py", "notification_service.py"],
        "src/bimas/utils": ["__init__.py", "file_utils.py", "date_utils.py", "validation.py"],
        "tests": ["__init__.py", "conftest.py"],
        "tests/unit": ["__init__.py", "test_agents.py", "test_rules.py", "test_security.py"],
        "tests/integration": ["__init__.py", "test_workflow.py", "test_api.py"],
        "tests/e2e": ["__init__.py", "test_complete_flow.py"],
        "tests/fixtures": ["sample_cases.json", "sample_policies.pdf", "mock_responses.json"],
        "data/policies": [],
        "data/cases": [],
        "data/uploads": [],
        "data/vector_store": [],
        "data/audit": [],
        "logs": [".gitkeep"],
        ".github/workflows": ["ci.yml", "deploy.yml", "security_scan.yml"],
        "k8s": ["deployment.yaml", "service.yaml", "configmap.yaml", "secret.yaml", "ingress.yaml"]
    }

    for folder, files in structure.items():
        # Create directory
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create files
        for file in files:
            file_path = folder_path / file
            if not file_path.exists():
                file_path.touch()
                print(f"Created: {file_path}")
            else:
                print(f"Skipped (exists): {file_path}")

if __name__ == "__main__":
    print("🚀 Starting project structure generation...")
    create_structure()
    print("✅ Project structure created successfully.")