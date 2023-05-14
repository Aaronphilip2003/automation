from django.shortcuts import render
from django.http import HttpResponse
import geopandas as gpd
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def say_hello(request):
    return HttpResponse("Hello World")

def proc(request):
    return render(request, 'hello.html')

def extract_points_within_polygon(dataset_path: str, point_path: str):
    # Load the input datasets
    dataset = gpd.read_file(dataset_path)
    point = gpd.read_file(point_path)
    
    # Loop over each admin ward polygon and extract points within it
    extracted_points = []
    for _, ward in dataset.iterrows():
        points_within_ward = point[point.within(ward.geometry)]
        extracted_points.append(points_within_ward)
    
    # Concatenate all extracted points and export to CSV
    extracted_points = pd.concat(extracted_points)
    extracted_points.to_csv("Extracted.csv", index=False)

def upload_files(request):
    if request.method == 'POST' and 'dataset' in request.FILES and 'point' in request.FILES:
        # Retrieve the uploaded files from the request
        dataset_file = request.FILES['dataset']
        point_file = request.FILES['point']

        # Check file extensions
        if not dataset_file.name.endswith('.shp') or not point_file.name.endswith('.shp'):
            return render(request, 'upload.html', {'error': 'Please upload only .shp files.'})

        # Instantiate FileSystemStorage
        fs = FileSystemStorage()

        # Run the extraction function
        print(dataset_file,point_file)
        extract_points_within_polygon(f"./{dataset_file}", f"./{point_file}")

        # Provide a download link for the generated file
        extracted_file_name = "Extracted.csv"
        extracted_file_url = fs.url(extracted_file_name)

        return render(request, 'result.html', {'extracted_file_url': '/download/'})


    return render(request, 'upload.html')   

def result_page(request):
    return render(request, 'result.html')

from django.http import FileResponse
import os

def download_extracted_file(request):
    # Define the file path of the extracted file
    file_path = os.path.join('./', 'Extracted.csv')

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Return the file as a response
            response = FileResponse(file, as_attachment=True, filename='Extracted.csv')
            return response
    else:
        # Handle the case when the file does not exist
        return HttpResponse("File not found")
