from supabase import create_client

SUPABASE_URL = "YOUR SUPABASE URL"
SUPABASE_KEY = "YOUR SUPABASE KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_data(column_name, new_data_list):

    print(f"\nUpdating '{column_name}' column with new data\n")
    response = supabase.table("fake_job").select("values").eq("name", column_name).execute()

    # Get jsonb column, default to empty list
    if response.data:
        for row in response.data:
            existing_list = row.get("values", []) 

    # Check if new data is not already in the list & update the list
    for item in new_data_list:

        if item not in existing_list:

            current_data = response.data[0]["values"] or []
            updated_data = current_data + new_data_list
            supabase.table("fake_job").update({"values": updated_data}).eq("name", column_name).execute()
            
        else:
            print(f"'{item}' already exists in the list. Skiping...")

    response = supabase.table("fake_job").select("values").eq("name", column_name).execute()
    print("\nUpdated data\n",response.data)
    print("\n\n")




# Add new data to the lists below
new_buzzwords = [
    'unlimited earnings', 'be your own boss', 'quick money', 
    'work from anywhere', 'instant profit', 'no experience needed',
    'weekly bonus', 'immediate start', 'flexible hours',
    'ground floor opportunity', 'million dollar',
    'passive income', 'financial freedom', 'dream lifestyle',
    'retire early', 'massive income', 'wealth system',
    'turnkey business', 'residual income', 'six figure income',
    'automated income', 'performance bonus', 'lifestyle business',
    'time freedom', 'unlimited potential', 'growing industry',
    'revolutionary opportunity', 'game changer', 'next big thing',
    'breakthrough system', 'exclusive opportunity'
    'easy money', 'get rich quick', 'no experience required',
    'no qualifications needed', 'no degree required', 'no experience necessary',
    'no experience needed', 'no qualifications required', 'no degree necessary',
    'very high pay', 'high salary', 'high income', 'huge earnings',
    'big money', 'quick cash', 'fast money', 'earn money fast',
    'earn money quickly', 'earn money easily', 'earn money fast'
]

new_red_flags = [
    'startup opportunity', 'ground floor', 'no office',
    'work from home only', 'commission only', 'investment required',
    'training fee', 'pyramid opportunity', 'multi-level marketing',
    'direct sales', 'independent distributor', 'recruitment bonus',
    'downline building', 'initial investment', 'buy-in required',
    'mandatory training cost', 'starter kit purchase', 'licensing fee',
    'certification required', 'equipment purchase needed',
    'business kit required', 'membership fee', 'registration cost',
    'processing fee', 'application fee', 'background check fee',
    'training materials cost', 'marketing package required',
    'website setup fee', 'inventory purchase required'
    ]

new_suspicious_email = [
    'temp', 'disposable', 'free', 'temporary', 
    'mailinator', 'guerrillamail', '10minutemail',
    'throwaway', 'yopmail', 'tempmail', 'trashmail',
    'fakeinbox', 'tempinbox', 'sharklasers', 'spam4.me',
    'dispostable', 'maildrop', 'mintemail', 'mohmal',
    'anonymbox', 'wegwerfemail', 'tempmail.net', 'burnermail',
    'emailondeck', 'tempmailer', 'instant-mail',
    'spamgourmet', 'maildrop.cc', 'mailnesia', 'maildrop.cc',
    'mailinator2.com', 'mailinator.com', 'mailinator.net',
    'temp-mail.org', 'temp-mail.ru', 'temp-mail.de',
    ]

new_urgency_phrases = [
    'limited time', 'urgent', 'immediate start', 
    'apply now', 'positions filling fast', 'today only',
    'last chance', 'deadline tomorrow',
    'act fast', 'dont miss out', 'closing soon',
    'limited spots', 'final call', 'expires tonight',
    'one time offer', 'while spots last', 'ending soon',
    'time sensitive', 'now or never', 'exclusive window',
    'limited availability', 'temporary opening', 'dont delay',
    'running out of time', 'offer expires', 'quick response needed'
    ]

# update_data("buzzwords", new_buzzwords)
# update_data("red_flags", new_red_flags)
# update_data("suspicious_email", new_suspicious_email)
# update_data("urgency_phrases", new_urgency_phrases)

# username = 'nitesh'
response = supabase.table("fake_job").select("values").execute()
print(response.data)
