from .models import Project, ProjectGroup


ecommerce_projects = [
    Project(
        project_id=1,
        name="Shoes Store",
        status="Proposal Sent",
        status_class="status-proposal",
        client="John Doe",
        price=558.00,
        designer_cost=31.00,
        start="-",
        end="-",
        days_left="Pending",
        days_left_class="project-pending",
        accepted=False
    ),

    Project(
        project_id=2,
        name="Beauty Store",
        status="Completed",
        status_class="status-completed",
        client="Smith Doe",
        price=1200.00,
        designer_cost=250.00,
        start="01/03/2026",
        end="25/03/2026",
        days_left="Completed",
        days_left_class="project-completed",
        accepted=True
    ),
    
    Project(
        project_id=3,
        name="Fashion Store",
        status="In Progress",
        status_class="status-in-progress",
        client="Doe Smith",
        price=1800.00,
        designer_cost=300.00,
        start="05/08/2026",
        end="30/09/2026",
        days_left="21 days",
        days_left_class="project-in-progress",
        accepted=True
    )
]


landing_pages_projects = [
    Project(
        project_id=4,
        name="Law Firm Website",
        status="In Progress",
        status_class="status-in-progress",
        client="Doe John",
        price=1500.00,
        designer_cost=200.00,
        start="10/07/2026",
        end="10/10/2026",
        days_left="31 days",
        days_left_class="project-in-progress",
        accepted=True
    ),

    Project(
        project_id=5,
        name="Accounting Website",
        status="Completed",
        status_class="status-completed",
        client="Adam Smith",
        price=900.00,
        designer_cost=150.00,
        start="25/05/2026",
        end="13/07/2026",
        days_left="Completed",
        days_left_class="project-completed",
        accepted=True
    )
]


project_groups = [
    ProjectGroup(
        group_id=1,
        name="E-commerce Websites",
        projects=ecommerce_projects
    ),

    ProjectGroup(
        group_id=2,
        name="Landing Pages",
        projects=landing_pages_projects
    )
]