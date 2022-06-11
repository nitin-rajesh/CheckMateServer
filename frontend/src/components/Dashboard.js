import React from "react";
import axios from "axios";

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
    const result = await axios.post("http://localhost:3000/orders");

    if (!result) {
      alert("Server error. Are you online?");
      return;
    }

    // Getting the order details back
    const { amount, id: order_id, currency } = result.data;

    const options = {
      key: "rzp_test_MtpbtcE1dAWxKC", // Enter the Key ID generated from the Dashboard
      amount: "80",
      currency: "INR",
      name: "Check Mate",
      description: "API key and per 100 calls",
      image: {},
      order_id: 2,
      handler: async function (response) {
        const data = {
          orderCreationId: 2,
          razorpayPaymentId: response.razorpay_payment_id,
          razorpayOrderId: response.razorpay_order_id,
          razorpaySignature: response.razorpay_signature,
        };

        // const result = await axios.post(
        //   "http://localhost:5000/payment/success",
        //   data
        // );

        // alert(result.data.msg);
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
        <table class="tg">
<thead>
  <tr>
    <th class="tg-c3ow">API_KEY</th>
    <th class="tg-c3ow">Status</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-c3ow">b804b707c355e0a3d86dfa24f34658b4c20298ee</td>
    <td class="tg-c3ow"><button><a href="https://rzp.io/i/DWTWY3ZA">Pay</a></button></td>
  </tr>
  <tr>
    <td class="tg-c3ow">d08d3ce2d0834b99489affd1aea3adb3edad9354</td>
    <td class="tg-c3ow"><button>Active</button></td>
  </tr>
  <tr>
    <td class="tg-c3ow">0958520a4c92c1ca3f2b0df4dead01cd07d16f3a</td>
    <td class="tg-c3ow"><button>Active</button></td>
  </tr>
  <tr>
    <td class="tg-c3ow">c9399e613f1ca616b0ef84e0569a4755bd644ddb</td>
    <td class="tg-c3ow"><button><a href="https://rzp.io/i/1mRxPQG4e">Pay</a></button></td>
  </tr>
</tbody>
</table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
