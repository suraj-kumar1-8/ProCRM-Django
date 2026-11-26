from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from crm.models import Customer, Lead, Activity


class Command(BaseCommand):
    help = "Populate the database with admin user and 25 Indian customers, 25 leads, and 30 interaction activities — all owned by admin."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding process..."))

        # 1. Create or get Admin Superuser (password: 123)
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("123")
            admin_user.email = "admin@procrm.in"
            admin_user.first_name = "Admin"
            admin_user.last_name = "Manager"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / 123"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))

        # 2. Seed 25 Indian Customers — all owned by admin
        customers_data = [
            {
                "name": "Aarav Sharma",
                "email": "aarav.sharma@tatasteel.co.in",
                "phone": "+91 22 6665 8282",
                "company": "Tata Steel Ltd",
                "address": "Bombay House, 24 Homi Mody Street, Fort, Mumbai, Maharashtra 400001",
            },
            {
                "name": "Priya Verma",
                "email": "priya.verma@infosys.com",
                "phone": "+91 80 2852 0261",
                "company": "Infosys Technologies",
                "address": "44 Electronics City, Hosur Road, Bengaluru, Karnataka 560100",
            },
            {
                "name": "Rohan Mehta",
                "email": "rohan.mehta@reliancejio.com",
                "phone": "+91 22 3555 5000",
                "company": "Reliance Jio Infocomm",
                "address": "Maker Chambers IV, Nariman Point, Mumbai, Maharashtra 400021",
            },
            {
                "name": "Sneha Iyer",
                "email": "sneha.iyer@wipro.com",
                "phone": "+91 80 2844 0011",
                "company": "Wipro Limited",
                "address": "Doddakannelli, Sarjapur Road, Bengaluru, Karnataka 560035",
            },
            {
                "name": "Vikram Singh Rathore",
                "email": "vikram.rathore@mahindra.com",
                "phone": "+91 22 2490 1441",
                "company": "Mahindra & Mahindra",
                "address": "Gateway Building, Apollo Bunder, Mumbai, Maharashtra 400001",
            },
            {
                "name": "Ananya Deshmukh",
                "email": "ananya.deshmukh@hdfcbank.com",
                "phone": "+91 22 3976 0000",
                "company": "HDFC Bank",
                "address": "HDFC Bank House, Senapati Bapat Marg, Lower Parel, Mumbai 400013",
            },
            {
                "name": "Arjun Nair",
                "email": "arjun.nair@techmahindra.com",
                "phone": "+91 20 6601 8100",
                "company": "Tech Mahindra",
                "address": "Rajiv Gandhi Infotech Park, Hinjewadi, Pune, Maharashtra 411057",
            },
            {
                "name": "Kavita Reddy",
                "email": "kavita.reddy@apollohospitals.com",
                "phone": "+91 44 2829 3333",
                "company": "Apollo Hospitals",
                "address": "21 Greams Lane, Off Greams Road, Chennai, Tamil Nadu 600006",
            },
            {
                "name": "Rajesh Gupta",
                "email": "rajesh.gupta@bhartiairtel.in",
                "phone": "+91 11 4666 6100",
                "company": "Bharti Airtel",
                "address": "Airtel Center, Plot No. 16, Udyog Vihar, Phase IV, Gurugram, Haryana 122015",
            },
            {
                "name": "Meera Joshi",
                "email": "meera.joshi@icicibank.com",
                "phone": "+91 22 2653 1414",
                "company": "ICICI Bank",
                "address": "ICICI Bank Tower, Bandra Kurla Complex, Mumbai, Maharashtra 400051",
            },
            {
                "name": "Siddharth Kapoor",
                "email": "siddharth.kapoor@flipkart.com",
                "phone": "+91 80 4985 2222",
                "company": "Flipkart Internet Pvt Ltd",
                "address": "Embassy Tech Village, Outer Ring Road, Devarabisanahalli, Bengaluru 560103",
            },
            {
                "name": "Deepika Chauhan",
                "email": "deepika.chauhan@sunpharma.com",
                "phone": "+91 22 4324 4324",
                "company": "Sun Pharmaceutical Industries",
                "address": "Sun House, Plot No. 201 B/1, Western Express Highway, Goregaon East, Mumbai 400063",
            },
            {
                "name": "Aditya Pandey",
                "email": "aditya.pandey@ola.in",
                "phone": "+91 80 6821 9500",
                "company": "Ola Cabs (ANI Technologies)",
                "address": "Tower C, Diamond District, Old Airport Road, Bengaluru, Karnataka 560008",
            },
            {
                "name": "Nisha Kulkarni",
                "email": "nisha.kulkarni@bajajfinserv.in",
                "phone": "+91 20 7157 6300",
                "company": "Bajaj Finserv Ltd",
                "address": "Bajaj Auto, Mumbai-Pune Road, Akurdi, Pune, Maharashtra 411035",
            },
            {
                "name": "Manish Tiwari",
                "email": "manish.tiwari@adanigroup.com",
                "phone": "+91 79 2555 7555",
                "company": "Adani Enterprises",
                "address": "Adani House, Near Mithakhali Circle, Navrangpura, Ahmedabad, Gujarat 380009",
            },
            {
                "name": "Pooja Saxena",
                "email": "pooja.saxena@zerodha.com",
                "phone": "+91 80 4040 2020",
                "company": "Zerodha Broking Ltd",
                "address": "153/154, 4th Cross, J.P. Nagar 4th Phase, Bengaluru, Karnataka 560078",
            },
            {
                "name": "Karan Malhotra",
                "email": "karan.malhotra@larsentoubro.com",
                "phone": "+91 22 6752 5656",
                "company": "Larsen & Toubro",
                "address": "L&T House, N.M. Marg, Ballard Estate, Mumbai, Maharashtra 400001",
            },
            {
                "name": "Ritu Agarwal",
                "email": "ritu.agarwal@zomato.com",
                "phone": "+91 124 490 9191",
                "company": "Zomato Ltd",
                "address": "Ground Floor, 12A, Meghdoot Building, Nehru Place, New Delhi 110019",
            },
            {
                "name": "Harsh Vardhan Patel",
                "email": "harsh.patel@amaboratory.co.in",
                "phone": "+91 79 2630 5000",
                "company": "Amba Research Labs",
                "address": "Sarkhej-Gandhinagar Highway, Near Karnavati Club, Ahmedabad, Gujarat 380015",
            },
            {
                "name": "Swati Mishra",
                "email": "swati.mishra@hcltech.com",
                "phone": "+91 120 438 2000",
                "company": "HCL Technologies",
                "address": "HCL Technology Hub, Plot No. 3A, Sector 126, Noida, Uttar Pradesh 201304",
            },
            {
                "name": "Dhruv Bhatt",
                "email": "dhruv.bhatt@razorpay.com",
                "phone": "+91 80 4609 7000",
                "company": "Razorpay Software Pvt Ltd",
                "address": "No. 22, 1st Floor, SJR Cyber, Laskar Hosur Road, Bengaluru, Karnataka 560034",
            },
            {
                "name": "Anjali Rao",
                "email": "anjali.rao@drreddy.com",
                "phone": "+91 40 4900 2900",
                "company": "Dr. Reddy's Laboratories",
                "address": "8-2-337, Road No. 3, Banjara Hills, Hyderabad, Telangana 500034",
            },
            {
                "name": "Nikhil Banerjee",
                "email": "nikhil.banerjee@itchotels.in",
                "phone": "+91 33 2249 7070",
                "company": "ITC Hotels",
                "address": "ITC Centre, 760 Anna Salai, Chennai, Tamil Nadu 600002",
            },
            {
                "name": "Tanvi Choudhary",
                "email": "tanvi.choudhary@policybazaar.com",
                "phone": "+91 124 468 4600",
                "company": "PolicyBazaar Insurance",
                "address": "Paisabazaar Building, Sector 44, Gurugram, Haryana 122003",
            },
            {
                "name": "Amit Kumar Singh",
                "email": "amit.singh@maruti.co.in",
                "phone": "+91 11 4678 1000",
                "company": "Maruti Suzuki India Ltd",
                "address": "Maruti Suzuki India, 1 Nelson Mandela Road, Vasant Kunj, New Delhi 110070",
            },
        ]

        created_customers = []
        for cdata in customers_data:
            customer, _ = Customer.objects.get_or_create(
                email=cdata["email"],
                defaults={**cdata, "owner": admin_user}
            )
            created_customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_customers)} customers."))

        # 3. Seed 25 Indian Leads — all owned by admin
        leads_data = [
            {
                "name": "Rahul Dravid",
                "email": "rahul.dravid@sportsinfra.in",
                "phone": "+91 80 2555 1234",
                "source": "Website",
                "status": "New",
                "notes": "Requested a product demo for sports academy management CRM module.",
                "customer": None,
            },
            {
                "name": "Neha Kakkar",
                "email": "neha.kakkar@tunein.in",
                "phone": "+91 22 4455 6677",
                "source": "Referral",
                "status": "Interested",
                "notes": "Looking for CRM solution for music label artist management. Budget approved for 50 seats.",
                "customer": None,
            },
            {
                "name": "Suresh Raina",
                "email": "suresh.raina@gracia.in",
                "phone": "+91 120 455 7890",
                "source": "Referral",
                "status": "Contacted",
                "notes": "Followed up on hospitality chain CRM requirements. Needs demo by end of month.",
                "customer": None,
            },
            {
                "name": "Aarav Sharma",
                "email": "aarav.sharma@tatasteel.co.in",
                "phone": "+91 22 6665 8282",
                "source": "Website",
                "status": "Converted",
                "notes": "Successfully signed enterprise contract for Tata Steel procurement team.",
                "customer": created_customers[0],
            },
            {
                "name": "Priya Verma",
                "email": "priya.verma@infosys.com",
                "phone": "+91 80 2852 0261",
                "source": "Cold Call",
                "status": "Converted",
                "notes": "Purchased annual license for Infosys BPO operations team.",
                "customer": created_customers[1],
            },
            {
                "name": "Farhan Akhtar",
                "email": "farhan.akhtar@excelentertain.in",
                "phone": "+91 22 2634 5678",
                "source": "Event",
                "status": "Interested",
                "notes": "Met at India Tech Summit 2026. Discussed content production workflow tools.",
                "customer": None,
            },
            {
                "name": "Divya Narayan",
                "email": "divya.narayan@chennaitech.in",
                "phone": "+91 44 2812 3456",
                "source": "Social Media",
                "status": "New",
                "notes": "Inquired via Instagram campaign about monthly subscription plans.",
                "customer": None,
            },
            {
                "name": "Rohan Mehta",
                "email": "rohan.mehta@reliancejio.com",
                "phone": "+91 22 3555 5000",
                "source": "Referral",
                "status": "Converted",
                "notes": "Direct executive referral. Converted to premier telecom enterprise account.",
                "customer": created_customers[2],
            },
            {
                "name": "Gaurav Tandon",
                "email": "gaurav.tandon@delhiuniv.ac.in",
                "phone": "+91 11 2766 7811",
                "source": "Website",
                "status": "Contacted",
                "notes": "Sent introductory capabilities deck for university administration CRM.",
                "customer": None,
            },
            {
                "name": "Sakshi Dhoni",
                "email": "sakshi.dhoni@7evenventures.in",
                "phone": "+91 651 234 5678",
                "source": "Social Media",
                "status": "Lost",
                "notes": "Project cancelled due to budget constraints at startup venture.",
                "customer": None,
            },
            {
                "name": "Sneha Iyer",
                "email": "sneha.iyer@wipro.com",
                "phone": "+91 80 2844 0011",
                "source": "Event",
                "status": "Converted",
                "notes": "Converted lead. Deploying CRM across Wipro's HR operations.",
                "customer": created_customers[3],
            },
            {
                "name": "Ravi Shankar Prasad",
                "email": "ravi.prasad@digitalgov.in",
                "phone": "+91 11 2301 9900",
                "source": "Website",
                "status": "Interested",
                "notes": "Evaluating CRM for Digital India government initiative. 200 user deployment.",
                "customer": None,
            },
            {
                "name": "Siddharth Kapoor",
                "email": "siddharth.kapoor@flipkart.com",
                "phone": "+91 80 4985 2222",
                "source": "Referral",
                "status": "Converted",
                "notes": "Onboarded as enterprise e-commerce client for seller management.",
                "customer": created_customers[10],
            },
            {
                "name": "Mira Rajput",
                "email": "mira.rajput@wellnessco.in",
                "phone": "+91 11 4567 8901",
                "source": "Cold Call",
                "status": "Contacted",
                "notes": "Spoke about wellness brand CRM for franchise management. Meeting scheduled.",
                "customer": None,
            },
            {
                "name": "Abhishek Bansal",
                "email": "abhishek.bansal@naukri.com",
                "phone": "+91 120 490 2222",
                "source": "Email Campaign",
                "status": "New",
                "notes": "Clicked link in Monsoon Product Update email campaign.",
                "customer": None,
            },
            {
                "name": "Lakshmi Menon",
                "email": "lakshmi.menon@keralaspices.in",
                "phone": "+91 484 237 5678",
                "source": "Website",
                "status": "Interested",
                "notes": "Interested in mobile field access and offline sync for spice export tracking.",
                "customer": None,
            },
            {
                "name": "Vivek Oberoi",
                "email": "vivek.oberoi@karrox.in",
                "phone": "+91 22 2878 5432",
                "source": "Other",
                "status": "Lost",
                "notes": "Selected another vendor due to pre-existing SAP integration commitment.",
                "customer": None,
            },
            {
                "name": "Vikram Singh Rathore",
                "email": "vikram.rathore@mahindra.com",
                "phone": "+91 22 2490 1441",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted enterprise lead. Mahindra auto dealership CRM deployment.",
                "customer": created_customers[4],
            },
            {
                "name": "Preeti Shenoy",
                "email": "preeti.shenoy@bookpalace.in",
                "phone": "+91 80 2655 7788",
                "source": "Cold Call",
                "status": "Contacted",
                "notes": "Discussed publisher inventory management and author tracking integration.",
                "customer": None,
            },
            {
                "name": "Meera Joshi",
                "email": "meera.joshi@icicibank.com",
                "phone": "+91 22 2653 1414",
                "source": "Referral",
                "status": "Converted",
                "notes": "Converted to client. ICICI Bank wealth management team onboarded.",
                "customer": created_customers[9],
            },
            {
                "name": "Ramesh Babu",
                "email": "ramesh.babu@hydsoftware.in",
                "phone": "+91 40 2335 9988",
                "source": "Event",
                "status": "New",
                "notes": "Exchanged cards at Hyderabad IT Expo 2026. Interested in startup plan.",
                "customer": None,
            },
            {
                "name": "Deepika Chauhan",
                "email": "deepika.chauhan@sunpharma.com",
                "phone": "+91 22 4324 4324",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted account. Deployed across 5 Sun Pharma regional offices.",
                "customer": created_customers[11],
            },
            {
                "name": "Yogesh Patel",
                "email": "yogesh.patel@surat textile.in",
                "phone": "+91 261 234 5678",
                "source": "Email Campaign",
                "status": "Lost",
                "notes": "Client postponed. Industry slowdown put all software purchases on hold.",
                "customer": None,
            },
            {
                "name": "Shreya Ghoshal",
                "email": "shreya.ghoshal@melodia.in",
                "phone": "+91 22 2431 7890",
                "source": "Social Media",
                "status": "Interested",
                "notes": "Requested a custom quote for 15 CRM team accounts for music production company.",
                "customer": None,
            },
            {
                "name": "Pooja Saxena",
                "email": "pooja.saxena@zerodha.com",
                "phone": "+91 80 4040 2020",
                "source": "Website",
                "status": "Converted",
                "notes": "Converted customer. Zerodha fintech operations team fully onboarded.",
                "customer": created_customers[15],
            },
        ]

        created_leads = []
        for ldata in leads_data:
            lead, _ = Lead.objects.get_or_create(
                email=ldata["email"],
                defaults={**ldata, "owner": admin_user}
            )
            created_leads.append(lead)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_leads)} leads."))

        # 4. Seed 30 Activities — all created by admin
        activity_templates = [
            ("Call", "Introductory phone consultation", "Called client to introduce ProCRM, assess their team size, and review expectations. Client responded very positively."),
            ("Meeting", "Executive CRM pipeline demonstration", "Presented live product walkthrough focusing on pipeline stages, customer profiles, and activity tracking."),
            ("Email", "Sent pricing proposal and timeline", "Emailed customized tier pricing sheet and standard terms of service. Offered a 14-day assisted setup period."),
            ("Call", "Contract clarification and security review", "Phone discussion with head of IT concerning data encryption, role permissions, and data isolation."),
            ("Meeting", "Weekly sales strategy check-in", "Met with account executives to align on quarterly revenue targets and pipeline deal velocity."),
            ("Note", "Customer requested invoice adjustment", "Client asked for annual invoicing upfront with GST identification included on bill."),
            ("Email", "Follow-up email on feature roadmap", "Replied with details regarding upcoming export capabilities and custom reporting widgets."),
            ("Call", "Quarterly customer success check-in", "Checked in on user adoption across teams. Overall satisfaction rating is 9.5/10."),
            ("Meeting", "Onboarding kickoff meeting", "Walked the leadership team through lead status transitions, customer data hygiene, and interaction logging."),
            ("Note", "Lead converted successfully to full account", "Customer profile created, primary contact designated, and introductory welcome package sent."),
        ]

        now = timezone.now()
        activities_count = 0

        for i, customer in enumerate(created_customers):
            num_acts = 1 if i % 2 == 0 else 2
            for j in range(num_acts):
                template = activity_templates[(i + j) % len(activity_templates)]
                act_date = now - timedelta(days=random.randint(1, 30), hours=random.randint(1, 12))

                linked_lead = customer.leads.first()

                Activity.objects.get_or_create(
                    customer=customer,
                    subject=f"{template[1]} - {customer.name}",
                    defaults={
                        "lead": linked_lead,
                        "activity_type": template[0],
                        "notes": template[2],
                        "date": act_date,
                        "created_by": admin_user,
                    }
                )
                activities_count += 1
                if activities_count >= 30:
                    break
            if activities_count >= 30:
                break

        self.stdout.write(self.style.SUCCESS(f"Seeded {activities_count} customer interaction activities."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
