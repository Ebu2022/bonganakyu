import pandas as pd
from django.core.management.base import BaseCommand
from chatbot.models import AttachmentOpportunity


class Command(BaseCommand):
    help = "Import attachment opportunities from Excel file"

    def handle(self, *args, **kwargs):
        file_path = "attachments.xlsx"  # Put Excel file in project root

        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            AttachmentOpportunity.objects.create(
                degree_programme=str(row["DEGREE PROGRAMME/COURSE"]).strip(),
                company_name=str(row["COMPANY PLACED"]).strip(),
                location=str(row["TOWN /COMPANY LOCATION"]).strip(),
                contact=str(row["COMPANY contact"]).strip(),
            )

        self.stdout.write(self.style.SUCCESS("Import completed successfully"))
