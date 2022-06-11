import React from 'react'
import axios from 'axios'

function Dashboard() {
	function loadScript(src) {
        return new Promise((resolve) => {
            const script = document.createElement("script");
            script.src = src;
            script.onload = () => {
                resolve(true);
            };
            script.onerror = () => {
                resolve(false);
            };
            document.body.appendChild(script);
        });
}

	async function displayRazorpay() {
        const res = await loadScript(
            "https://checkout.razorpay.com/v1/checkout.js"
        );

        if (!res) {
            alert("Razorpay SDK failed to load. Are you online?");
            return;
        }

        // creating a new order
        const result = await axios.post("http://localhost:5000/payment/orders");

        if (!result) {
            alert("Server error. Are you online?");
            return;
        }

        // Getting the order details back
        const { amount, id: order_id, currency } = result.data;

        const options = {
            key: "rzp_test_MtpbtcE1dAWxKC", // Enter the Key ID generated from the Dashboard
            amount: amount.toString(),
            currency: currency,
            name: "Check Mate",
            description: "API key and per 100 calls",
            image: {},
            order_id: order_id,
            handler: async function (response) {
                const data = {
                    orderCreationId: order_id,
                    razorpayPaymentId: response.razorpay_payment_id,
                    razorpayOrderId: response.razorpay_order_id,
                    razorpaySignature: response.razorpay_signature,
                };

                const result = await axios.post("http://localhost:5000/payment/success", data);

                alert(result.data.msg);
            },
            prefill: {
                name: "Check Mate",
                email: "CheckMate@example.com",
                contact: "9999999999",
            },
            notes: {
                address: "Bengaluru",
            },
            theme: {
                color: "#61dafb",
            },
        };

        const paymentObject = new window.Razorpay(options);
        paymentObject.open();
}
  return (
	<div className="auth-wrapper">
	<div className="auth-inner">
	<div>
		<table>
			<thead>
				<tr>
					<th>API</th>
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>isbfoubfobsofbsobfowbfowbf</td>
					<td><button>
						Pay
						</button></td>
				</tr>
			</tbody>
		</table>
	</div>
		</div>
		</div>
  )
}

export default Dashboard