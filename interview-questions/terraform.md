# Terraform interview questions
 - What is Terraform and why is it used?
   Ans: Terraform is open source IaC tool, used to create, maintain infra across different public clouds like AWS/Azure/GCP
 - What is Infrastructure as Code (IaC)?
   Ans: Maintaining infra through code for repeatability, versioning etc
 - How does Terraform work internally?
   Ans: Terraform uses providers provided by cloud platforms, using these terraform HCL code is converted into API call to spin up infra.
 - What are providers in Terraform?
   Ans: Providers are plugins which convert terraform code to API call to be performed on cloud.
 - What is a Terraform state file?
   Ans: State file refers to current infra setup, it will be created once terraform apply is run, it is also used to find diff between current and desired infra setup during terrafrom plan
 - Why is state file important in Terraform?
   Ans: It is used to find diff between current and desired infra setup during terrafrom plan
 - What is the difference between terraform plan and apply?
   Ans: 
   plan - prints out infra setup that will be created/modified/deleted, it wont actually do any changes to infra. terraform plan -out output.tf
   apply - applies modifications like create/modify/delete infra. terraform apply output.tf
 - What is terraform init? 
   Ans: looks into providers mentioned and downloads them into workspace.
 - What are modules in Terraform?
   Ans: Modules are used to create reusable peices of code. example: create VPC module and use it while creating VMs.
 - How do you reuse code using modules?
   Ans:
   module {
    name: "VPC",
    cidr: 10.0.0.1/24,
    .....
   }
   in another tf file, how to call this?

 - What is remote backend in Terraform?
   Ans: remote backend is used to store statefile, it will be helpful in locking the file when already a session is open. This helps in statefile edit without corruption.
 - Why should we store state file remotely?
   Ans: it will be helpful in locking the file when already a session is open. This helps in statefile edit without corruption.
 - What is state locking in Terraform?
   Ans: it will be helpful in locking the file when already a session is open. This helps in statefile edit without corruption.
 - What is the difference between count and for_each?
   Ans: count is used in scenarios where n number of vms are to be created without writing th vm code block n times
   for_each is also used for same but this will loop through some list
   lets say we have env - dev/test/uat/prod and want to create 
 - What are variables and outputs in Terraform?
   Ans: 
 - How do you manage secrets in Terraform?
 - How do you provision AWS resources using Terraform?
 - What are common issues with Terraform in production?
 - How do you handle drift in Terraform?
   Ans: Drift happens when someone changes infra manually outside terraform, terraform plan will provide the diff between expected and present infra.
 - What are best practices for Terraform in AWS?