import tkinter as tk

def calculate_bond_price(face_value, coupon_rate, maturity_period, yield_to_maturity):
   coupon_payment = face_value * coupon_rate
   price = 0.0

   for i in range(maturity_period):
        price += coupon_payment / (1 + yield_to_maturity) ** (i + 1)
   price += face_value / (1 + yield_to_maturity) ** maturity_period

   return price

def calculate_yield_to_maturity(face_value, coupon_rate, maturity_period, bond_price):
    coupon_payment = face_value * coupon_rate
    yield_to_maturity = 0.05  # Initial guess
    tolerance = 0.00001
    max_iterations = 1000

    for _ in range(max_iterations):
        estimate = 0.0
        derivative = 0.0
        for i in range(maturity_period):
            estimate += coupon_payment / (1 + yield_to_maturity) ** (i + 1)
            derivative -= (i + 1) * coupon_payment / (1 + yield_to_maturity) ** (i + 2)
        estimate += face_value / (1 + yield_to_maturity) ** maturity_period
        derivative -= maturity_period * face_value / (1 + yield_to_maturity) ** (maturity_period + 1)

        # Update yield to maturity using Newton's method
        yield_to_maturity -= (estimate - bond_price) / derivative

        if abs(estimate - bond_price) < tolerance:
            return yield_to_maturity
        
    raise ValueError("Yield to maturity calculation did not converge.")

def calculate_duration(face_value, coupon_rate, maturity_period, yield_to_maturity):
    coupon_payment = face_value * coupon_rate
    price = calculate_bond_price(face_value, coupon_rate, maturity_period, yield_to_maturity)
    duration = 0.0

    for i in range(maturity_period):
        weight = coupon_payment / (1 + yield_to_maturity) ** (i + 1)
        duration += (i + 1) * weight 
    weight = face_value / (1 + yield_to_maturity) ** maturity_period
    duration += maturity_period * weight
    duration /= price

    return duration

def calculate_convexity(face_value, coupon_rate, maturity_period, yield_to_maturity):
    coupon_payment = face_value * coupon_rate
    price = calculate_bond_price(face_value, coupon_rate, maturity_period, yield_to_maturity)
    convexity = 0.0

    for i in range(maturity_period):
        weight = coupon_payment / (1 + yield_to_maturity) ** (i + 1)
        convexity += weight * (i + 1) * (i + 2)
    weight = face_value / (1 + yield_to_maturity) ** maturity_period
    convexity += maturity_period ** 2 * weight
    convexity /= price
    convexity /= (1 + yield_to_maturity) ** 2

    return convexity

def calculate():
    try:
        face_value = float(face_value_entry.get())
        coupon_rate = float(coupon_rate_entry.get())
        maturity_period = int(maturity_period_entry.get())
      
        if calculation_type.get() == "Price":
            yield_to_maturity = float(ytm_entry.get())
            bond_price = calculate_bond_price(face_value, coupon_rate, maturity_period, yield_to_maturity)
            duration = calculate_duration(face_value, coupon_rate, maturity_period, yield_to_maturity)
            convexity = calculate_convexity(face_value, coupon_rate, maturity_period, yield_to_maturity)
            result_label.config(text=f"Bond Price: {bond_price:.2f}\nDuration: {duration:.2f}\nConvexity: {convexity:.2f}")

        elif calculation_type.get() == "Yield":
            bond_price = float(bond_price_entry.get())
            ytm = calculate_yield_to_maturity(face_value, coupon_rate, maturity_period, bond_price)
            duration = calculate_duration(face_value, coupon_rate, maturity_period, yield_to_maturity)
            convexity = calculate_convexity(face_value, coupon_rate, maturity_period, yield_to_maturity)
            result_label.config(text=f"Yield to Maturity: {yield_to_maturity:.4f}\nDuration: {duration:.2f}\nConvexity: {convexity:.2f}")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def update_ui():
    if calculation_type.get() == "Price":
        ytm_label.grid(row=4, column=0, padx=5, pady=5)
        ytm_entry.grid(row=4, column=1, padx=5, pady=5)
        bond_price_label.grid_forget()
        bond_price_entry.grid_forget()
    elif calculation_type.get() == "Yield":
        bond_price_label.grid(row=4, column=0, padx=5, pady=5)
        bond_price_entry.grid(row=4, column=1, padx=5, pady=5)
        ytm_label.grid_forget()
        ytm_entry.grid_forget()


    # Create the main window
root = tk.Tk()
root.title("Bond Calculator")

# Create and place widgets   
calculation_type = tk.StringVar(value="Price")

tk.Label(root, text="Calculation Type:").grid(row=0, column=0, padx=5, pady=5)
dropdown = tk.OptionMenu(root, calculation_type, "Price", "Yield", command=lambda _: update_ui())
dropdown.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Face Value:").grid(row=1, column=0, padx=5, pady=5)
face_value_entry = tk.Entry(root)
face_value_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Coupon Rate (as decimal):").grid(row=2, column=0, padx=5, pady=5)
coupon_rate_entry = tk.Entry(root)
coupon_rate_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Maturity Period (Years):").grid(row=3, column=0, padx=5, pady=5)
maturity_period_entry = tk.Entry(root)
maturity_period_entry.grid(row=3, column=1, padx=5, pady=5)

ytm_label = tk.Label(root, text="Yield to Maturity:")
ytm_entry = tk.Entry(root)

bond_price_label = tk.Label(root, text="Bond Price:")
bond_price_entry = tk.Entry(root)

tk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=2, padx=5, pady=5)  

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

update_ui()  # Initial UI update based on default selection

root.mainloop()
