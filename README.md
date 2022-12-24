<h1 align="center" id="title">Strikify</h1>

<p align="center"><img src="https://socialify.git.ci/uamadasun/strikify/image?description=1&amp;descriptionEditable=The%20web%20application%20that%20turns%20any%20phone%20into%20a%20point%20of%20sale&amp;font=Jost&amp;name=1&amp;theme=Light" alt="project-image"></p>

<p id="description">This web app utilizes the Strike API to facilitate lightning payments so merchants can get paid in their local currency. I was inspired to create this web application by small business owners who are charged high fees on card payments by companies such as Visa and Mastercard. The Strike API provides an option for these small business owners to use a cheaper payment rail via the Bitcoin lightning network.</p>

<h2>🧐 Features</h2>

Here are some of the project's best features:

*   Merchants can register to use the Strikify app using their Strike app username.
*   Merchants can add a new shop and add products to their shop
*   Merchants can take orders, checkout customers and receive payment instantly all from the Strikify app.

  
<h2>💻 Technologies used:</h2>

*   Python
*   Strike API
*   HTML5
*   bCrypt
*   Session
*   Bootstrap
*   CSS 3
*   MySQL

<h2>Demo</h2>

<h3>Log In:</h3>
<p>Merchants can register for a Strikify account only if they have a Strike account. Log in is secured with BCrypt and session. Upon login, new users are directed to create their shop.</p>
<img src="https://media.giphy.com/media/3t7PrpazAocBFhPo09/giphy.gif" alt="login and registration"/>

<h3>Create a new shop</h3>
<p>The shop owner is then prompted to enter their shop's name. After entering their shop name, they can add products to their shop!</p>
<img src="https://media.giphy.com/media/QdtrfHKyo90hIp2csI/giphy.gif" alt="add a new shop"/>

<h3>Add Products</h3>
<p>Our shop owner is now able to add products to their shop! On this page, they also have the ability to edit and delete their product offerings.</p>
<img src="https://media.giphy.com/media/wOtf7qIDUbb73wGSST/giphy.gif" alt="adding products"/>

<h3>Add to Cart & Checkout</h3>
<p>Once our shop owner gets a new customer order, they head to the order page, add the items to cart, checkout, and select "Generate Invoice" in order to generate a lightning invoice. The Strike API generates the lightning invoice and the shop owner is directed to a page with the generated QR code. The customer can then use any lightning wallet on their own device to pay the invoice. The payment will be received in the shop owner's Strike account instantly. </p>
<img src="https://media.giphy.com/media/AhlgR8KZafoj52VWbu/giphy.gif" alt="order and checkout"/>



<h2>:ledger: Future Features</h2>

- [ ] Timer that counts down how long the customer has before the lightning invoice expires (invoice must be paid within 2 minutes or the shop owner has to generate a new invoice)
- [ ] Webhook to redirect customer after successful payment or expiration of lightning invoice
- [ ] Cosmetic UI improvement


<h2>🛡️ License:</h2>

This project is licensed under the GNU General Public License v3.0
