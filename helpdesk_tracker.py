from datetime import datetime


class Ticket:
  ticket_counter = 1

  def __init__(self, title, category, priority):
    self.id = Ticket.ticket_counter
    Ticket.ticket_counter += 1
    self.title = title
    self.category = category  # e.g., Network, Software, Hardware
    self.priority = priority  # Low, Medium, High, Critical
    self.status = "Open"  # Open, In Progress, Resolved
    self.created_at = datetime.now()
    self.resolved_at = None

  def resolve_ticket(self):
    self.status = "Resolved"
    self.resolved_at = datetime.now()

  def get_duration(self):
    if self.resolved_at:
      return str(self.resolved_at - self.created_at).split(".")[0]
    else:
      return str(datetime.now() - self.created_at).split(".")[0] + " (Ongoing)"


class HelpDeskSystem:

  def __init__(self):
    self.tickets = []

  def create_ticket(self):
    print("\n--- Create New Support Ticket ---")
    title = input("Enter issue summary (e.g., VPN connection failed): ")
    category = input("Enter category (Network/Hardware/Software): ")
    priority = input("Enter priority (Low/Medium/High/Critical): ")

    new_ticket = Ticket(title, category, priority)
    self.tickets.append(new_ticket)
    print(
        f"[Success] Ticket #{new_ticket.id} created successfully with Status:"
        f" Open."
    )

  def view_tickets(self):
    if not self.tickets:
      print("\n[Info] No tickets found in the system.")
      return

    print("\n--- Support Tickets Dashboard ---")
    print(
        f"{'ID':<4} | {'Title':<25} | {'Category':<10} | {'Priority':<10} |"
        f" {'Status':<10} | {'Age/Duration':<15}"
    )
    print("-" * 80)
    for t in self.tickets:
      print(
          f"{t.id:<4} | {t.title:<25} | {t.category:<10} | {t.priority:<10} |"
          f" {t.status:<10} | {t.get_duration():<15}"
      )

  def update_ticket_status(self):
    self.view_tickets()
    if not self.tickets:
      return

    try:
      tid = int(input("\nEnter Ticket ID to update status: "))
      ticket = next((t for t in self.tickets if t.id == tid), None)

      if ticket:
        print("1. Set to 'In Progress'")
        print("2. Set to 'Resolved' (Close Ticket)")
        choice = input("Choose action (1/2): ")

        if choice == "1":
          ticket.status = "In Progress"
          print(f"[Success] Ticket #{tid} status updated to 'In Progress'.")
        elif choice == "2":
          ticket.resolve_ticket()
          print(
              f"[Success] Ticket #{tid} marked as 'Resolved'. SLA Target met."
          )
        else:
          print("[Error] Invalid choice.")
      else:
        print("[Error] Ticket ID not found.")
    except ValueError:
      print("[Error] Please enter a valid number.")


def demo_helpdesk():
  system = HelpDeskSystem()
  print("--- Automated Helpdesk Demonstration ---")

  # Simulating ticket creation programmatically so it runs cleanly in Colab
  t1 = Ticket("Network switch failure at Branch A", "Network", "High")
  t2 = Ticket("Email login timeout for user", "Software", "Medium")
  system.tickets.extend([t1, t2])

  print(f"[Info] Created 2 sample tickets automatically.")
  system.view_tickets()

  print("\n[Action] Resolving Ticket #1...")
  t1.resolve_ticket()
  system.view_tickets()


if __name__ == "__main__":
  demo_helpdesk()
