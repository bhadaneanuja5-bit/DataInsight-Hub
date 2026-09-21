from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Dataset

import pandas as pd


# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    return render(
        request,
        'analytics/home.html'
    )


# ==========================================
# REGISTER
# ==========================================

def register(request):

    message = ""

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        if not username or not password:

            message = (
                "Username and password are required."
            )

        elif password != confirm_password:

            message = (
                "Passwords do not match."
            )

        elif User.objects.filter(
            username=username
        ).exists():

            message = (
                "Username already exists."
            )

        else:

            user = User.objects.create_user(
                username=username,
                password=password
            )

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

    return render(
        request,
        'analytics/register.html',
        {
            'message': message
        }
    )


# ==========================================
# LOGIN
# ==========================================

def user_login(request):

    message = ""

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

        else:

            message = (
                "Invalid username or password."
            )

    return render(
        request,
        'analytics/login.html',
        {
            'message': message
        }
    )


# ==========================================
# LOGOUT
# ==========================================

def user_logout(request):

    logout(request)

    return redirect(
        'home'
    )


# ==========================================
# UPLOAD DATASET
# ==========================================

def upload_dataset(request):

    # User must be logged in
    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    message = ""

    if request.method == 'POST':

        file = request.FILES.get(
            'dataset'
        )

        if file:

            description = request.POST.get(
                'description',
                ''
            )

            dataset = Dataset.objects.create(

                user=request.user,

                name=file.name,

                description=description,

                file=file

            )

            return redirect(
                'dataset_analysis',
                dataset_id=dataset.id
            )

    return render(
        request,
        'analytics/upload.html',
        {
            'message': message
        }
    )


# ==========================================
# DATASET LIST
# ==========================================

def dataset_list(request):

    # User must be logged in
    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    datasets = Dataset.objects.filter(
        user=request.user
    ).order_by(
        '-uploaded_at'
    )

    return render(
        request,
        'analytics/dataset_list.html',
        {
            'datasets': datasets
        }
    )


# ==========================================
# DATASET ANALYSIS
# ==========================================

def dataset_analysis(
    request,
    dataset_id
):

    # User must be logged in
    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    # Only allow the logged-in user
    # to access their own dataset

    dataset = get_object_or_404(
        Dataset,
        id=dataset_id,
        user=request.user
    )


    # --------------------------------
    # READ CSV FILE
    # --------------------------------

    df = pd.read_csv(
        dataset.file.path
    )


    # --------------------------------
    # BASIC DATASET INFORMATION
    # --------------------------------

    rows = len(df)

    columns = len(
        df.columns
    )

    column_names = list(
        df.columns
    )


    # --------------------------------
    # MISSING VALUES
    # --------------------------------

    missing_values = (
        df.isnull()
        .sum()
        .to_dict()
    )

    total_missing_values = int(
        df.isnull()
        .sum()
        .sum()
    )


    # --------------------------------
    # MISSING DATA PERCENTAGE
    # --------------------------------

    total_cells = rows * columns

    if total_cells > 0:

        missing_percentage = round(

            (
                total_missing_values
                / total_cells
            ) * 100,

            2

        )

    else:

        missing_percentage = 0


    # --------------------------------
    # NUMERIC COLUMNS
    # --------------------------------

    numeric_columns = (

        df.select_dtypes(
            include='number'
        )

        .columns

        .tolist()

    )

    numeric_column_count = len(
        numeric_columns
    )


    # --------------------------------
    # CHART DATA
    # --------------------------------

    chart_data = []

    chart_x_column = ""

    chart_y_column = ""


    if len(numeric_columns) >= 2:

        if (

            'R&D Spend'
            in numeric_columns

            and

            'Profit'
            in numeric_columns

        ):

            chart_x_column = (
                'R&D Spend'
            )

            chart_y_column = (
                'Profit'
            )

        else:

            chart_x_column = (
                numeric_columns[0]
            )

            chart_y_column = (
                numeric_columns[1]
            )


        chart_data = (

            df[
                [
                    chart_x_column,
                    chart_y_column
                ]
            ]

            .dropna()

            .round(2)

            .to_dict(
                'records'
            )

        )


    # --------------------------------
    # STATISTICAL SUMMARY
    # --------------------------------

    numeric_summary = (

        df.describe()

        .round(2)

        .to_dict()

    )


    # --------------------------------
    # AUTOMATIC DATA INSIGHTS
    # --------------------------------

    insights = []


    for column in numeric_columns:

        average = round(
            df[column].mean(),
            2
        )

        minimum = round(
            df[column].min(),
            2
        )

        maximum = round(
            df[column].max(),
            2
        )

        insights.append({

            'column':
                column,

            'average':
                average,

            'minimum':
                minimum,

            'maximum':
                maximum

        })


    # --------------------------------
    # HIGHEST AVERAGE COLUMN
    # --------------------------------

    highest_average_column = ""

    highest_average_value = 0


    if numeric_columns:

        average_values = {}


        for column in numeric_columns:

            average_values[column] = (
                df[column].mean()
            )


        highest_average_column = max(

            average_values,

            key=average_values.get

        )

        highest_average_value = round(

            average_values[
                highest_average_column
            ],

            2

        )


    # --------------------------------
    # LOWEST AVERAGE COLUMN
    # --------------------------------

    lowest_average_column = ""

    lowest_average_value = 0


    if numeric_columns:

        average_values = {}


        for column in numeric_columns:

            average_values[column] = (
                df[column].mean()
            )


        lowest_average_column = min(

            average_values,

            key=average_values.get

        )

        lowest_average_value = round(

            average_values[
                lowest_average_column
            ],

            2

        )


    # --------------------------------
    # AUTOMATIC OBSERVATION
    # --------------------------------

    observations = []


    if total_missing_values == 0:

        observations.append(
            "The dataset has no missing values."
        )

    else:

        observations.append(

            f"The dataset contains "
            f"{total_missing_values} "
            f"missing values."

        )


    if numeric_column_count > 0:

        observations.append(

            f"The dataset contains "
            f"{numeric_column_count} "
            f"numeric column(s)."

        )


    if highest_average_column:

        observations.append(

            f"{highest_average_column} "
            f"has the highest average value "
            f"among numeric columns."

        )


    if lowest_average_column:

        observations.append(

            f"{lowest_average_column} "
            f"has the lowest average value "
            f"among numeric columns."

        )


    # --------------------------------
    # DATA PREVIEW
    # --------------------------------

    data_preview = (

        df.head(10)

        .values

        .tolist()

    )


    # --------------------------------
    # SEND DATA TO HTML
    # --------------------------------

    context = {

        'dataset':
            dataset,

        'insights':
            insights,

        'rows':
            rows,

        'columns':
            columns,

        'column_names':
            column_names,

        'missing_values':
            missing_values,

        'total_missing_values':
            total_missing_values,

        'missing_percentage':
            missing_percentage,

        'numeric_columns':
            numeric_columns,

        'numeric_column_count':
            numeric_column_count,

        'highest_average_column':
            highest_average_column,

        'highest_average_value':
            highest_average_value,

        'lowest_average_column':
            lowest_average_column,

        'lowest_average_value':
            lowest_average_value,

        'observations':
            observations,

        'numeric_summary':
            numeric_summary,

        'data_preview':
            data_preview,

        'chart_data':
            chart_data,

        'chart_x_column':
            chart_x_column,

        'chart_y_column':
            chart_y_column,

    }


    return render(

        request,

        'analytics/analysis.html',

        context

    )