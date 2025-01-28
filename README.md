# Dormeal
### Restaurant delivery for students and restaurants on campus.
www.dormeal.com

iOS Application: [Dormeal2.0](https://github.com/AnthonyCampos1234/Dormeal2.0)

Dormeal is a gig-based food delivery service web application that allows users to order food from selected restaurants located on their campus, and have that food delivered to them 
by fellow students for much lower costs than would otherwise be charged by alternative services like doordash or uber eats.
## Theory and Business Strategy

Dormeal operates in a market similar to DoorDash and Uber Eats, where food delivery is typically a highly competitive space. However, by focusing exclusively on college campuses, we lower key barriers to entry for delivery workers (dashers). Here’s how:

- **Lower Barriers for Dashers**: On a campus, dashers don’t need cars, bikes, or scooters—they can walk. This increases the supply of available dashers.
- **Increased Delivery Efficiency**: With a geographically condensed delivery area, each dasher can complete more orders in less time, increasing efficiency.
- **Lower Delivery Costs**: These factors allow us to lower delivery costs significantly, making our $5 delivery value proposition realistic.

Together, these elements help Dormeal achieve a sustainable, affordable delivery model tailored to college campuses.

## Software

### Frontend
- The frontend is built using HTML, CSS, and JavaScript. Styling is stored in the [static](https://github.com/IpDaniel/dormeal/tree/main/static) folder, and templates are in the [templates](https://github.com/IpDaniel/dormeal/tree/main/templates) folder.
- External CSS libraries are used to enhance the styling.
- JavaScript is used to handle animations and send data to the backend via AJAX.
- Payments are processed through the Stripe API for secure transactions.

### Backend
- The backend is powered by the Flask framework (Python). Routes for handling web requests are defined in the [app.py](https://github.com/IpDaniel/dormeal/blob/main/app.py) file.
- Payments are processed using the Stripe API to ensure secure and reliable transactions.
- Dashers are notified about new delivery requests through an automatic email system, with the functionality located in the [mvp_emailer.py](https://github.com/IpDaniel/dormeal/blob/main/scripts/mvp_emailer.py) file.

### Deployment

Dormeal is currently deployed through PythonAnywhere, and can be accessed by visiting the domain www.dormeal.com
