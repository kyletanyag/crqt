<template>
<div>
  <img alt="CRQT logo" src="../assets/CRQT.png" height="300" style="margin-bottom:50px">
  <hr>
  <h1 class="pt-2 , heading">Welcome to the Cyber Resilience Quantification Tool</h1>
    <div class="row mx-5">
      <div class="col-6 text-left">
        <h3 class="subheading">Purpose</h3>
        <p class="text-justify">
          As new technology emerges, cyber-criminals become more creative in penetrating vulnerable systems changing their attack methods for different security systems. 
          The Cyber Resilience Quantification Tool (CRQT) helps to fortify a system's resiliency by taking in the customer's unique network topology, analyzing computation, 
          networking, and physical vulnerabilities, and prescribing mitigation remedies to fortify customer systems and make them more resilient. Protecting cyber network 
          infrastructures is essential, but it remains a balancing act between security versus cost. By developing a tool that will help stakeholders foresee possible attacks 
          and prioritize vulnerabilities by criticality, stakeholders (cybersecurity professionals and decision-makers) will be able to conduct cost-benefit risk assessments 
          of their CPS networks to address their organization's security thresholds and objectives. 
        </p>
      </div>
      <div class="col-6 text-center">
          <img class="image1" alt="Lock Image" src="../assets/lock.png"  height="300">
      </div>
    </div>
    <hr>
    <div class="row mx-5">
      <div class="col-6 text-center">
          <img class="image2" alt="Lock Image" src="../assets/ModelDriven.png"  >      
      </div>
      <div class="col-6 text-left">
        <h3 class="subheading">Model-Driven Component</h3>
        <p class="text-justify">
        The model-driven component is a user generated network based on the National Institute of Standards and Technology (NIST) Control Systems  Security Program Recommended Architecture. This input methodology will allow users to create a hypothetical network by selecting individual network components. In the model-driven approach, an end-user will select common network components of different models from various manufacturers. Combining all the chosen network components will create a generalized network graph, and that information is then sent to the CRQT simulation engine to conduct a cyber resiliency assessment.         </p>
      </div>
    </div>
    <hr>
    <div class="row mx-5">
      <div class="col-6 text-left">  
        <h3 class="subheading">Data-Driven Component</h3>
        <p class="text-justify">
           The network topology (data-driven) input UI is an interface that allows for a user to input a network topology from an existing network infrastructure. The customer defines the methodology that inputs LAGs as "data-driven" as the LAGs derive from an existing network probed via a scanner tool (Nessus/OpenVAS). The data is collected and then converted into a LAG using the Multi-host, Multi-stage Vulnerability Analysis Language (MulVAL). Lag’s represent all network paths and encodes the causality relationship among configuration settings and potential attacker privileges.
        </p>           
      </div>
      <div class="col-6 text-left">
          <img class="image3" alt="Lock Image" src="../assets/Mulval.png"  height="300">
      </div>
    </div>
</div>

 </template>

<script>

</script>

<style>
.heading {
  margin-top: 30px;
  margin-bottom: 30px;
  font-family:  Helvetica, sans-serif;

}
.subheading{
  margin-top: 30px;
  margin-bottom: 30px;
  font-family:  Helvetica, sans-serif;
  text-decoration-line: underline;
}
.image1{
  margin-top:30px ;
}
.image2 {
  height: 700px;
  object-fit: contain;
}
.image3 {
  width: 600px;
  object-fit: contain;
}
</style>
