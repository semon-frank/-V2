# SmartMigrator

SmartMigrator is a Windows system migration and restore tool designed for
safe testing, staged restoration, and large-scale file validation.

It supports:
- Full system scan
- Rule-based restore blueprints
- Dry-run and test-clean restore modes
- Large-scale batch restoration with failure tracking

## Current Status
This is a **public testing version**.
The goal is to evaluate real-world demand and usability.

## Usage (V2)

```bash
python main_v2.py scan
python generate_blueprint_v2.py
python restore_execute_v2.py --dry-run
python restore_execute_v2.py --limit 5000 --test-clean

