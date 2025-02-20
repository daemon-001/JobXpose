from supabase import create_client

SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_data(column_name, new_data):

    response = supabase.table("fake_job").select("values").eq("name", column_name).execute()

    if response.data:
        current_data = response.data[0]["values"] or []
        updated_data = current_data + new_data
        supabase.table("fake_job").update({"values": updated_data}).eq("name", column_name).execute()

        response = supabase.table("fake_job").select("values").eq("name", column_name).execute()
        print(response)

    else:
        print("No data found")


# Add new data to the lists below
new_buzzwords = [

    ]

new_red_flags = [

    ]

new_suspicious_email = [

    ]

new_urgency_phrases = [

    ]

update_data("buzzwords", new_buzzwords)
update_data("red_flags", new_red_flags)
update_data("suspicious_email", new_suspicious_email)
update_data("urgency_phrases", new_urgency_phrases)
