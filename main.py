#!/usr/bin/env python3

import os
import shutil
import argparse
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File categories and their extensions
FILE_CATEGORIES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.json'],
}

def create_directories(base_path, categories):
    """Create directories for each category if they don't exist"""
    for category in categories:
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            logging.info(f"Created directory: {category_path}")

def get_category(file_extension):
    """Determine the category of a file based on its extension"""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return 'others'

def organize_files(source_dir, target_dir=None, recursive=False, dry_run=False, stats=True):
    """Organize files from source directory into categories in target directory"""
    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist!")
        return

    # If target directory is not specified, use source directory
    if target_dir is None:
        target_dir = source_dir

    # Create category directories
    create_directories(target_dir, list(FILE_CATEGORIES.keys()) + ['others'])

    # Statistics
    file_stats = {category: 0 for category in FILE_CATEGORIES.keys()}
    file_stats['others'] = 0
    total_files = 0
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Skip target subdirectories if source and target are the same
        if source_dir == target_dir:
            for category in list(FILE_CATEGORIES.keys()) + ['others']:
                if os.path.join(source_dir, category) in [os.path.join(root, d) for d in dirs]:
                    dirs.remove(category)
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip files in the target categories if source and target are the same
            if source_dir == target_dir and any(category in file_path for category in list(FILE_CATEGORIES.keys()) + ['others']):
                continue
            
            # Get file extension and category
            _, file_extension = os.path.splitext(file)
            category = get_category(file_extension)
            
            # Destination path
            dest_path = os.path.join(target_dir, category, file)
            
            # Handle file name conflicts
            if os.path.exists(dest_path):
                filename, extension = os.path.splitext(file)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_filename = f"{filename}_{timestamp}{extension}"
                dest_path = os.path.join(target_dir, category, new_filename)
            
            # Move the file
            if not dry_run:
                try:
                    shutil.move(file_path, dest_path)
                    logging.info(f"Moved: {file_path} -> {dest_path}")
                except Exception as e:
                    logging.error(f"Error moving {file_path}: {e}")
                    continue
            else:
                logging.info(f"Would move: {file_path} -> {dest_path}")
            
            # Update statistics
            file_stats[category] += 1
            total_files += 1
        
        # If not recursive, break after the first level
        if not recursive:
            break
    
    # Print statistics
    if stats and total_files > 0:
        print("\n" + "="*50)
        print("File Organization Statistics")
        print("="*50)
        for category, count in file_stats.items():
            if count > 0:
                print(f"{category.capitalize()}: {count} files")
        print(f"Total files organized: {total_files}")
        print("="*50)
        
        # Save statistics to file if not in dry run mode
        if not dry_run:
            stats_file = os.path.join(target_dir, "organization_stats.json")
            stats_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_directory": source_dir,
                "target_directory": target_dir,
                "files_organized": file_stats,
                "total_files": total_files
            }
            with open(stats_file, 'w') as f:
                json.dump(stats_data, f, indent=4)
            logging.info(f"Statistics saved to {stats_file}")
    
    if total_files == 0:
        logging.info("No files were found to organize.")

def main():
    parser = argparse.ArgumentParser(description="Organize files into categories based on file type")
    parser.add_argument("source", help="Source directory to organize")
    parser.add_argument("-t", "--target", help="Target directory (default: same as source)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Show what would be done without actually moving files")
    parser.add_argument("-n", "--no-stats", action="store_true", help="Don't show statistics")
    
    args = parser.parse_args()
    
    organize_files(args.source, args.target, args.recursive, args.dry_run, not args.no_stats)

if __name__ == "__main__":
    main()
