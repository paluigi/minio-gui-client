import flet as ft
from minio import Minio

def main(page: ft.Page):

    endpoint = ft.TextField(label="Endpoint")
    access_key = ft.TextField(label="Access Key")
    secret_key = ft.TextField(label="Secret Key", password=True)
    secure = ft.Checkbox(label="Secure", value=True)
    view_list = ft.ListView(expand=True)


    def list_buckets(e):
        try:
            minio = Minio(
                endpoint=endpoint.value,
                access_key=access_key.value,
                secret_key=secret_key.value,
                secure=secure.value,
            )
            buckets = minio.list_buckets()
            buckets = [bucket.name for bucket in buckets]
            view_list.controls = [ft.Text(
                value="Buckets",
                size=30,
                weight=ft.FontWeight.BOLD
                )
            ]
            view_list.controls.extend([
                ft.ElevatedButton(text=bucket, data=bucket, on_click=list_files) 
                for bucket in buckets]
            )
            page.update()
        except Exception as e:
            page.open(
                ft.AlertDialog(
                    title=ft.Text(value=f"Error: {e}"),
                )
            )
    

    def list_files(e):
        bucket = e.control.data
        try:
            minio = Minio(
                endpoint=endpoint.value,
                access_key=access_key.value,
                secret_key=secret_key.value,
                secure=secure.value,
            )
            file_list = minio.list_objects(bucket)
            file_list = [file.object_name for file in file_list]
            view_list.controls = [ft.Text(
                value="Files",
                size=30,
                weight=ft.FontWeight.BOLD
                )
            ]
            view_list.controls.extend([
                ft.ElevatedButton(text=file, data=file) 
                for file in file_list]
            )
            page.update()
        except Exception as e:
            page.open(
                ft.AlertDialog(
                    title=ft.Text(value=f"Error: {e}"),
                )
            )
    
    
    list_buckets_btn = ft.ElevatedButton(text="List buckets", on_click=list_buckets)
    

    page.add(
        ft.SafeArea(
            ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(
                                value="Minio GUI Client",
                                size=50,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text("Minimal GUI application to explore files on Minio")
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            endpoint,
                            access_key,
                            secret_key,
                            secure
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            list_buckets_btn
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            view_list
                        ]
                    )
                ],
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )
    page.scroll = ft.ScrollMode.AUTO


ft.app(main)
