const DataDrivenResultOptions = 
  [
    {
      title: 'Summary',
      description: "Contains a quick summary of the network's components and connections.",
      routeName: 'Data Driven Results - Summary'
    },
    {
      title: 'Overall Network Compromise',
      description: "Discusses a network's overall compromise & exploitation metrics. \
        Contains information about a network's risk and severity statistics.",
      routeName: 'Data Driven Results - Overall Network Compromise'
    },
    {
      title: 'Network Visualization',
      description: "Produces a graph reprsentation of a network for visualization. \
        You can visually depict how a network is set up as well as see the related \
        meta-data and computed scores associated with each node in the network.",
      routeName: 'Data Driven Results - Network Visualization'
    },
    {
      title: 'Derived Node Exploitation',
      description: "Contains specific data and statistics on derived nodes in a \
        network such as a breakdown of what priviledges an attacker gains by reaching \
        a specific derived node as well as the number of conditions and rules needed \
        to be satisfied before reaching a derived node.",
      routeName: 'Data Driven Results - Derived Node Exploitation'
    },
    {
      title: 'Recommendations',
      description: "Outlines recommendations for increasing your cyber-resiliency.\
        The recommendations highlight which derived fact nodes are the most vulnerable \
        and which vulnerabilities have the highest computed base scores.",
      routeName: 'Data Driven Results - Recommendations'
    },
    {
      title: 'Printout',
      description: 'A page containing the full printout of all the simulation results.',
      routeName: 'Data Driven Results - Printout'
    }
  ]

  const ModelDrivenResultOptions = 
  [
    {
      title: 'Summary',
      description: "Contains a quick summary of all the network's components and connections, \
        a breakdown of the number of nodes at each layer, and the overall security of the network.",
      routeName: 'Model Driven Results - Summary'
    },
    {
      title: 'Network Visualization',
      description: "Produces a graph reprsentation of a network for visualization. \
        You can visually depict how a network is set up following NIST's control system \
        security recommended architecture as well as see the related meta-data and \
        computed scores associated with each node in the network.",
      routeName: 'Model Driven Results - Network Visualization'
    },
    {
      title: 'Graph Metrics',
      description: "Produces metrics related to the network graph such as the degree\
        closeness, betweeness, PageRank, and Katz centrality.",
      routeName: 'Model Driven Results - Graph Metrics'
    },
    {
      title: 'Attack Path Metrics',
      description: "You can input a target node in the network and path metrics to that node will be calculated \
        such as the number of possible attack paths to that node, the base, exploitability, and impact scores of \
        each path, and the top exploitable and impactful paths in the network.",
      routeName: 'Model Driven Results - Attack Path Metrics'
    },
    {
      title: 'Severity Display',
      description: "Denotes the severity levels of every node-to-node connection or edge in the network.",
      routeName: 'Model Driven Results - Severity Display'
    },
    {
      title: 'Recommendations',
      description: "Outlines recommendations for increasing your cyber-resiliency by applying the \
        the TOPSIS method. The TOPSIS method assesses device criticality by building on the concept\
        that the chosen alternative should have the shortest geometric distance from the positive \
        ideal solution and the largest geometric distance from the negative ideal solution.",
      routeName: 'Model Driven Results - Recommendations'
    },
    {
      title: 'Printout',
      description: 'A page containing the full printout of all the simulation results \
        except for attack path specific data. Unfortunately, we are unable to contain \
        that in the printout page due to the massive number of possible attack paths.',
      routeName: 'Model Driven Results - Printout'
    }
  ]

export {
  DataDrivenResultOptions,
  ModelDrivenResultOptions
};