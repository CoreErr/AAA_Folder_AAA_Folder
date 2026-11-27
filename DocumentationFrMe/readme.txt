      Helm Chart
          │
          ↓
  Helm rendering
          │
          ↓
rendered Kubernetes YAML
          │
          ↓
    parser.py
          │
          ↓
Python dictionaries
          │
          ↓
    models.py
          │
          ↓
  ResourceNode objects
          │
          ↓
  graph_builder.py
          │
          ↓
Kubernetes resource graph
          │
          ↓
      Rules
          │
┌────────┴────────┐
↓                 ↓
HPA-PDB rule     Other rules
│                 │
└────────┬────────┘
          ↓
  conflict report

======================================================
PROJECT ARCHITECTURE & HELM ANALYSIS FRAMEWORK GUIDE
======================================================

1. UNPACKED SOURCE CHART (setup_helm/charts/nginx/)
------------------------------------------------------
- How it got there : Created when you ran `helm pull 
                     bitnami/nginx --untar`.
- What it contains : Raw, unrendered Helm templates 
                     (templates/), chart metadata 
                     (Chart.yaml), and default 
                     configuration settings (values.yaml).
- Role in project  : Template source code containing 
                     Go syntax ({{ .Values... }}). 
                     Your analyzer cannot directly 
                     analyze this directory because 
                     values are not evaluated yet.


2. RENDERED TARGET MANIFESTS (setup_helm/rendered/)
------------------------------------------------------
- How they got there:

  * `rendered/nginx.yaml` was created by your manual 
    command: `helm template > ./rendered/nginx.yaml`

  * `rendered_manifests/test-nginx.yaml` was generated 
    by running `helmChartGet.py`.

- What they contain : Standard, flat Kubernetes YAML 
                     manifests with all variable 
                     placeholders resolved into concrete 
                     values.
- Role in project  : These rendered .yaml files serve 
                     as your primary input. Your Python 
                     analyzer, Checkov, KubeLinter, and 
                     KICS will inspect these files to 
                     build dependency graphs and run rules.


3. CUSTOM ANALYSIS FRAMEWORK (Root Files & rules/)
------------------------------------------------------
- parser.py        : Uses `ruamel.yaml` or `PyYAML` to 
                     parse the rendered YAML manifests 
                     into structured Python dicts.

- models.py        : Defines data structures representing 
                     Kubernetes resources, selectors, and 
                     graph node models.

- graph_builder.py : Reads parsed resources and builds 
                     a `networkx` directed graph 
                     connecting related objects (e.g., 
                     HPA -> Deployment <- PDB).

- rules/hpa_pdb.py : Implements your deterministic 
                     operational constraint logic to 
                     flag when `PDB.minAvailable > 
                     HPA.minReplicas`.

- rules/base.py    : Abstract base class defining 
                     standard methods every rule must 
                     implement (e.g., severity rating).

- main.py          : Entry point executing the parser, 
                     building the dependency graph, 
                     running rules, and outputting 
                     the analysis report.


===========================================================
===========================================================

===========================================================
===========================================================

🔴 TIER 1 — MUST UNDERSTAND

1. Kubernetes:
   Pod
   Deployment
   Service
   HPA
   PDB
2. Kubernetes YAML:
   apiVersion
   kind
   metadata
   spec
3. Labels + selectors
4. HPA ↔ workload relationship
   PDB ↔ Pod relationship
5. Static analysis concept
6. The actual HPA/PDB conflict

🟠 TIER 2 — NEED TO UNDERSTAND BEFORE IMPLEMENTING

7. Helm:
   Chart
   templates
   values
   rendering
8. Multi-document YAML
9. Python nested dictionaries
10. Python classes/objects/methods/inheritance
11. Graph:
    nodes
    directed edges
    relationships
12. NetworkX basics

🟡 TIER 3 — LEARN WHILE BUILDING

13. ResourceNode model
14. Rule/base-rule architecture
15. Rule execution
16. Error handling
17. Logging
18. CLI arguments
19. Test cases
20. Output/report formatting

===========================================================
===========================================================

===========================================================
===========================================================

Hypervisor Is a sw.
  tht manages Hardware
of a computer
It slices up the hardware like
  cpu
  mem
  hdd
To make smol virtual
  hardware boxes
So now our VM can use it and run as a
  containerized
form of OS

Hardware of Infra As a Code
50 physical computer,
  calD as "Bare Metal" server
Each comp is bolted on a
  rack
Each comp as Hypervisor OS installed

Hyper visors report to
  central manager API
like VMware vCenter

Whc begs the question, wh is IaC?
Is managing & supplying
  IT infrastrc like
virt Machine,
networks,
storage,
load balancers,
kubernet clusters

Hw does IaC happen
Thru a .yaml/.tf file
Tht specifies wh
  hardware comp is needed
EX:
# A declarative recipe for your infrastructure
server:
  type: cloud-vm-large
  count: 3
  open_ports: [80, 443]
database:
  engine: postgresql
  storage: 100GB
Then give this file to
  amaozn/google
cloud provider

Managing file wtot Terraform
* **State Mgmt Flaw:** Naive scripts lack state memory, causing accidental duplicate builds and bloated cloud bills on re-run.
* **Dry-Run Flaw:** Running raw scripts blind directly on prod can accidentally wipe resources without prior impact previews.
* **Graph Ordering Flaw:** Hardcoding hacky `sleep()` timers in scripts leads to race conds and broken resource dependencies.
* **Drift Detection Flaw:** Rogue 3 AM web console tweaks go untracked, causing mystery outages and broken env parity.
* **Multi-Cloud Flaw:** Devs waste time learning 3 different vendor-locked tools (CloudFormation, ARM/Bicep, GCP DM) instead of 1 workflow.

Hashi Corp's "Terraform"
Is a Iac(Infrastrc as Code) tool
It allows for
  desc specific IaC
then allows for
  creating,
  changing,
  deleting
tht infraStruc autoMtCle
Works wt Git to allow for
  stt mgmt
  dry-run before exeCtn
  dependency graph orderG
  drift detection
  mult cloud stdZtn
Is "Outer IaC" as they
  work wt
baremetal server, VM
and installs K8s cluster

Def Kubernetes
CalD as K8s
Manages thousands of
  live containers
accross dozens of
  physical/virt servers

Def Containers
    - Prbl
If sw ran in dev comp, but
not on live server.
It was the fault of
  missing sys lib
  diff py/node ver
  conflictG Os settGs
   - Container
PkgS code wt things like
  libs,
  config files
  sys binaries
into a single isolated pkg
CalD as Image/Container
Containers r made using Docker

Def Kubernetes Cluster Grp of netwkD servers(virt/phy)
Cluster is a grp of std
  linux serv linked
together
So they act like 1 gaint server
WHERE,
1 serv is Control Plane
Other serv are worker nodes

Def Kubernetes Control Plane
Manages cluster stt
Schedules workloads
Coordinates ctrls

Def Kubernetes Worker Nodes

Def Inner IaC & its Scope
Defines Pods/Deployments
Configures HPAs/PDBs
Creates Ingress Routing Rules

Def Kubernetes cluster
Uses many clusters
Cluster is a group of
  VM wt kubernetes setup
Created from a YAML file

3 Main stuff in K8s
  MAIN
Node > server
Pod > Logical Section
  of the Node's resrc
Container > Sandbox for the applKsn
  HOLDS THEM TOGETHER
ReplicaSet
Labels & Selectors

Def YAML file
YAML file is the written
  confiGtn of settings
Can be .pdf, .xml, .json file

Def Kubernetes Manifests
Are YAML files tht desc
  workloads
  containers
  cluster resrcs
Applied thru Kuberntes API

Def Manifest / Resource in K8s
Is the instrucTn/
Tht desc desired stt of
  appKsn/cluster comp
Rather than step-by-step instruc
Thus calD 'Declarative'
Using whc, kubernetes
  acts and decides wh to do whr

Key Struc of Manfiest
~ ex:
apiVersion: <api-group>/<version> # 1. API endpoint ver
kind: <ResourceKind>              # 2. Type of Kubernetes obj
metadata:                         # 3. Ide and orgZtn tags
  name: <resource-name>
  namespace: <namespace-name>     # Optional
  labels:
    app: <app-name>               # Tags used by selTrs to link resrc
  annotations:
    <key>: <value>                # Info metadata for ext tools
spec:                             # 4. Desired operaTnl stt
  # Resource-specific para go here
                                         
List Manifest / Resource & Def what it desc
  Deployment
How many Pod replicas should run;
how to roll out updates
  Service
How to reach the appKsn thru
a stable network endpoint
  HPA
When to increase or decrease
the no of replicas
  PDB
How many Pods can be voluntarily
disrupted during maintenance

Def Deployment Manifest in K8s
DefD thru YAML file
Is the config inside YAML file
  tht kubernets works with
Creates, manages & updates the pod
Detects worker node crashes
  recreates pods on another node
Whn we release a update, it
  updates pods one by one
  so users dont get downtime

Pods r mortal, they die, get reassigned to diff ips and continue this flow

Def Service Manifest
Give permanant
  ip addr & domain name
fr a defined Pod
So it doesnt matter if its
  in this node or that node
Acts as a load balancer tht
  distributes worload to pods
~ ex:
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  selector:
    app: payment
    # Links this Service to
    # Pods with label app=payment
  ports:
    - port: 8080

Def HPA(Horizontal Pod Autoscaler) Manifest
Works in Deploymment?
Scales no of pods in DplyMt bsd on
  comp resrc like
cpu,gpu,mem & cust metrics
This scaling is done dynamic,
  ex: whn traffic is low the
pod is scaled down to 1
Wh it increases it is increased
  up to 5 if load increases
Responds to user Traffic
~ ex:
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-hpa
spec:
  scaleTargetRef:
    kind: Deployment
    name: payment-service
    # DirTy tgts the Dplymnt
  minReplicas: 1
  # Can shrink down to 1
  # pod at night!
  maxReplicas: 5

Def PDB(Pod Disruptio Budget) Manifest
Lim no. of pods that can be down
during a update/maintenance
Responds to admin maintenance
  hw much risk can we take
during upgrades

Def ReplicaSet
Created & Manged by DeplyMt
Is too a manifest file & ctrlr
  - Behavior
If Current < Desired: It calls the Kubernetes API: "Launch 'N' new Pods immediately
If Current > Desired: It calls the Kubernetes API: "Terminate 'N' excess Pods
If Current == Desired: It does nothing and waits for the next check
Each replicaset ver reprsnts
  ver of app from old to new

Def Labels & Selectors
  Labels
Metadata attached to obj
Id/tags to refer to specific type
of pods
  Selectors
Queries that find obj bsd
on that metadata.
Works like a filter

Every single YAML file shares this structure
apiVersion: apps/v1   # 1. Which version of the K8s API understands this file?
kind: Deployment      # 2. What type of object are we creating?
metadata:             # 3. What is its name and how do we tag it?
  name: payment-dep
  labels:
    app: payment
spec:                 # 4. What is the actual configuration/recipe?
  replicas: 3
  ...

Def Resource Object in K8s
It is the specific manifest
  stored in K8s cluster
Can be said 2 be instance of
  manifests like
    DeplyMt
    Serice
    PBD
    HPA

HPA ↔ Workload Relationships
PDB ↔ Pod Relationships

Abv relationships too complicated for pleb like me, ignoring it


Helm
Like a Pkg Manager of K8
Instead of applKsn ver & stuff
  it lists Configurations
fr K8s clusters

Helm Chart
StrucTd folder on Disk
Contains configs to
  deply an applKsn K8s

values.yaml
Configuration for K8s


templates/

ex:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicaCount }}  # <--- Plugs in value from values.yaml!
  template:
    spec:
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}

Rendering in Helm
Combining
  placeholders inside
    "templates/"
  wt variables inside
    "values.yaml"
Whc generates a pure std K8s YAML



uwa uwa, python notes lost

Def cmplxity
Symptons ofcmplxTy
Hw to solve cmplxTy
1. Reduce cmplxTy
2. Encapsulate cmplxTy so users donnt hv to deal wt it

Def Dependency
Dependency types
  3
  internal
  interface lvl(frontend & api)
  external(outside lib)

Def Coupling


## 1. Kubernetes resource model — 🔴 absolutely essential

You need to understand:

```text
Kubernetes Cluster
│
├── Node 1
│   └── Pods
│
├── Node 2
│   └── Pods
│
└── Node 3
    └── Pods
```

And especially:

```text
Deployment
    ↓ creates/manages
Pods
```

Then:

```text
HPA
    ↓ scales
Deployment / Pods

PDB
    ↓ constrains voluntary disruption
Pods
```

And:

```text
Service
    ↓ selects
Pods
```

You don't need to know Kubernetes internals yet.

### You should be able to answer:

> "What is a Deployment?"
> "What is a Pod?"
> "Why does an HPA exist?"
> "Why does a PDB exist?"
> "How does a Kubernetes object identify/select another set of objects?"

That last question leads directly to labels/selectors.
---

# 2. Kubernetes YAML structure — 🔴 absolutely essential

You need to become comfortable looking at something like:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-app

spec:
  replicas: 3

  selector:
    matchLabels:
      app: my-app

  template:
    metadata:
      labels:
        app: my-app
```

And mentally translate:

```text
YAML
 ↓
Kubernetes resource
 ↓
Deployment
 ↓
desired state:
    3 replicas
 ↓
Pods have:
    app = my-app
```

You should understand the difference between:

```yaml
metadata:
spec:
```

and that `spec` means roughly:
> "What state/configuration do I want this resource to have?"
You **don't** need to memorize every Kubernetes YAML field.

---

# 3. Labels + selectors — 🔴 VERY important for your project

This is probably the most important Kubernetes concept specifically for your analyzer.

Example:

```yaml
Deployment:
  labels:
    app: payment

Service:
  selector:
    app: payment
```

Meaning:

```text
Service
   │
   │ selector: app=payment
   ↓
Deployment's Pods
   app=payment
```

Your graph builder is basically going to discover relationships like this.

You need to understand:

```text
label
selector
matchLabels
matchExpressions
target references
```

at least conceptually.

---

# 4. HPA + PDB themselves — 🔴 VERY important

Before touching Python code, understand the actual conflict.

For example:

```yaml
HPA:
    minReplicas: 1
    maxReplicas: 10
```

means roughly:

```text
Don't normally scale below 1
Don't normally scale above 10
```

While:

```yaml
PDB:
    minAvailable: 2
```

means roughly:

```text
During voluntary disruption,
keep at least 2 Pods available.
```

Therefore:

```text
HPA says:
    minimum = 1

PDB says:
    minimum available = 2
```

Potential problem:

```text
HPA scales → 1 Pod

Node maintenance starts
        ↓
Kubernetes wants to evict Pod
        ↓
PDB says:
"NO, I need 2 available"
        ↓
Only 1 exists
        ↓
Eviction blocked
```

And **this is the fundamental thing your detector is trying to discover from static configuration**.

---

# 5. Understand what "static analysis" means — 🔴 VERY important

This is another foundational concept.

Normally:

```text
YAML
 ↓
Kubernetes
 ↓
actual cluster
 ↓
observe behavior
```

Your project instead does:

```text
YAML
 ↓
Analyzer
 ↓
detect suspicious relationships
```

No cluster required.

Think:

```text
Source code analyzer:
    code → AST → rules → bugs

Your analyzer:
    Kubernetes YAML → resource model/graph → rules → conflicts
```

That's the central architecture.

---

# 6. Helm — 🟠 important, but don't learn all of Helm

Your current:

> "using helm somehow works"

is exactly where I'd spend a little time.

Helm is basically a **Kubernetes application packaging + templating system**.

Instead of giving you a giant pile of fixed YAML:

```text
deployment.yaml
service.yaml
hpa.yaml
...
```

a Helm chart can contain templates:

```yaml
replicas: {{ .Values.replicas }}
```

and values:

```yaml
replicas: 3
```

Helm combines these:

```text
Helm Chart
   +
values/configuration
   ↓
Helm template rendering
   ↓
ordinary Kubernetes YAML
```

So your analyzer ideally doesn't have to understand Helm's templating language.

It analyzes the **rendered output**:

```text
Helm chart
     ↓
helm template
     ↓
rendered YAML
     ↓
YOUR ANALYZER
```

This is a VERY important architectural distinction.

### You need to understand:

```text
Chart
Template
values.yaml
Helm rendering
Rendered Kubernetes manifests
```

You don't need to become a Helm expert.

---

# 7. Python OOP — 🟠 important

You already know programming/Python, so this shouldn't be a huge learning block.

You need enough to understand:

```python
class ResourceNode:
    ...
```

and:

```python
class Rule:
    ...
```

and things like:

```python
rule.check(graph)
```

You should understand:

```text
class
object
attribute
method
constructor
inheritance
abstract/base class
```

Especially this architecture:

```text
BaseRule
   ↑
   │
HPAPDBRule
```

Meaning:

```text
BaseRule
    defines common interface

HPAPDBRule
    implements specific logic
```

---

# 8. Python dictionaries / nested data — 🟠 VERY important

This may actually matter more than advanced OOP.

After YAML parsing, you're probably dealing with structures resembling:

```python
{
    "apiVersion": "autoscaling/v2",
    "kind": "HorizontalPodAutoscaler",
    "metadata": {
        "name": "my-app"
    },
    "spec": {
        "minReplicas": 1,
        ...
    }
}
```

You need to be comfortable navigating:

```python
resource["kind"]

resource["metadata"]["name"]

resource["spec"]["minReplicas"]
```

and handling missing fields safely.

Because your parser's job is basically:

```text
YAML text
   ↓
Python dict/list structures
```

---

# 9. YAML parsing with PyYAML — 🟠 important

You don't need to learn YAML specification deeply.

You need to understand:

```text
YAML file
    ↓
YAML parser
    ↓
Python objects
```

For example:

```yaml
kind: Deployment
metadata:
  name: payments
```

becomes approximately:

```python
{
    "kind": "Deployment",
    "metadata": {
        "name": "payments"
    }
}
```

### One important thing for YOUR project:

Kubernetes manifests often contain:

```yaml
---
apiVersion: ...
kind: Deployment
...
---
apiVersion: ...
kind: Service
...
---
apiVersion: ...
kind: HorizontalPodAutoscaler
...
```

That's a **multi-document YAML file**.

Your parser therefore needs to conceptually do:

```text
file
 ↓
document 1
document 2
document 3
...
 ↓
Python dictionaries
```

Understand this before vibe-coding `parser.py`.

---

# 10. Graph theory — 🟠 important, but only basic graph theory

Don't go study an entire graph-theory course.

You mainly need:

```text
Graph
Node
Edge
Directed graph
Traversal
```

Your project's graph might look like:

```text
Deployment
    ↑
    │ manages
    │
   HPA

Deployment
    │
    │ Pods have labels
    ↓
   PDB
```

Or conceptually:

```text
[Deployment]
     ↑
     │ target
     │
    [HPA]

[Deployment]
     │
     │ selected pods
     ↓
    [PDB]
```

The point of the graph is:

> Instead of treating YAML files as unrelated blobs, represent the relationships between Kubernetes resources explicitly.

That's what `networkx` is helping you do.

---

# 11. NetworkX — 🟡 understand the concept, not the library internals

You don't need to understand how NetworkX internally implements graphs.

You DO need to understand what your code is asking it to do.

Something conceptually like:

```python
graph.add_node(deployment)
graph.add_node(hpa)

graph.add_edge(hpa, deployment)
```

means:

```text
graph

HPA ─────→ Deployment
```

Then your rules can inspect:

```text
HPA
 ↓
related Deployment
 ↓
related PDB
```

Learn the small subset of NetworkX your project uses.

---

# 12. Your project's data model — 🟡 important

This is where `models.py` starts making sense.

Instead of passing raw dictionaries everywhere:

```python
resource["metadata"]["name"]
resource["spec"]["minReplicas"]
...
```

you can create something like:

```text
ResourceNode
│
├── kind
├── name
├── namespace
├── labels
├── selectors
├── spec
└── relationships
```

Then your program can work with:

```python
node.kind
node.name
node.selectors
```

instead of constantly digging through YAML dictionaries.

Understand **why this abstraction exists**.

---

# 13. Rule-engine architecture — 🟡 important

This is the part that makes your project extensible.

You don't want:

```python
if HPA and PDB:
    check conflict

if Service and Deployment:
    check something

if X and Y:
    check something
```

all dumped into `main.py`.

Instead:

```text
rules/
│
├── base.py
├── hpa_pdb.py
├── service_deployment.py
└── ...
```

Conceptually:

```text
                 Rule
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
     HPA-PDB   Service-X   Rule-X
```

Each rule answers:

> "Given the resource graph, does this particular known bad relationship exist?"

---

# 14. Main pipeline — 🟢 now everything connects

Eventually you should be able to draw your entire project like this:

```text
             Helm Chart
                 │
                 ↓
          Helm rendering
                 │
                 ↓
       rendered Kubernetes YAML
                 │
                 ↓
            parser.py
                 │
                 ↓
        Python dictionaries
                 │
                 ↓
            models.py
                 │
                 ↓
         ResourceNode objects
                 │
                 ↓
         graph_builder.py
                 │
                 ↓
       Kubernetes resource graph
                 │
                 ↓
              Rules
                 │
        ┌────────┴────────┐
        ↓                 ↓
    HPA-PDB rule      Other rules
        │                 │
        └────────┬────────┘
                 ↓
          conflict report
```

**That is the architecture you should understand before vibe-coding.**

---

# So, your learning priority

If I were putting this into an actual learning queue for **you**, I'd make it:

```text
🔴 TIER 1 — MUST UNDERSTAND

1. Kubernetes:
   Pod
   Deployment
   Service
   HPA
   PDB

2. Kubernetes YAML:
   apiVersion
   kind
   metadata
   spec

3. Labels + selectors

4. HPA ↔ workload relationship
   PDB ↔ Pod relationship

5. Static analysis concept

6. The actual HPA/PDB conflict


🟠 TIER 2 — NEED TO UNDERSTAND BEFORE IMPLEMENTING

7. Helm:
   Chart
   templates
   values
   rendering

8. Multi-document YAML

9. Python nested dictionaries

10. Python classes/objects/methods/inheritance

11. Graph:
    nodes
    directed edges
    relationships

12. NetworkX basics


🟡 TIER 3 — LEARN WHILE BUILDING

13. ResourceNode model

14. Rule/base-rule architecture

15. Rule execution

16. Error handling

17. Logging

18. CLI arguments

19. Test cases

20. Output/report formatting
```

## And what you DON'T need beforehand

Don't get trapped thinking you need:

```text
❌ Kubernetes administration
❌ Kubernetes networking in depth
❌ Docker expertise
❌ Linux administration
❌ Cloud architecture
❌ Helm internals
❌ Advanced graph theory
❌ Advanced Python
❌ Machine learning
❌ Kubernetes source code
❌ NetworkX internals
```

For this project, **you are building a static relationship analyzer, not becoming a Kubernetes administrator.**

---

## The biggest conceptual jump for you

Your current understanding is:

```text
YAML
 ↓
settings for computers
```

I'd upgrade it to:

```text
Kubernetes YAML
 ↓
declarative descriptions of RESOURCES
 ↓
Kubernetes interprets those descriptions
 ↓
resources interact through explicit relationships
 ↓
actual workloads emerge from those relationships
```

And your analyzer does:

```text
Kubernetes YAML
 ↓
"understand what resources exist"
 ↓
"understand how they relate"
 ↓
"look for known dangerous combinations"
 ↓
report them
```

That's a **much better mental model** for vibe-coding this.

### If you want to start coding soon

I'd **not** start with `parser.py`.

First get to the point where you can manually look at ~4 tiny YAML files:

```text
Deployment
HPA
PDB
Service
```

and draw:

```text
HPA ─────→ Deployment
              ↑
              │
             PDB

Service ─────→ Pods
```

Then you can look at `parser.py`, `models.py`, and `graph_builder.py` and understand **why they exist**, rather than asking AI to generate four mysterious files that happen to work.

That is the sweet spot for vibe-coding this project.

Good Mind Map to get started wt this project

@startmindmap
* IT Infrastructure & IaC
** 1. Physical Infrastructure
*** Bare-Metal Servers
**** Physical computers
**** Mounted in racks
**** Hardware resources
***** CPU
***** Memory (RAM)
***** HDD / SSD
***** Network
*** Hypervisor
**** Software layer over hardware
**** Creates & manages VMs
**** Allocates virtual CPU, RAM, storage
**** Examples
***** VMware ESXi
***** KVM
*** Centralized Management
**** VMware vCenter
**** Manages multiple hypervisors / hosts

** 2. Infrastructure as Code (Outer IaC)
*** Definition
**** Manage infrastructure using code
**** Provision, modify & destroy resources
*** Infrastructure Resources
**** Physical / Virtual Machines
**** Networks
**** Storage
**** Load Balancers
**** Kubernetes Clusters
*** IaC Configuration
**** YAML / HCL / JSON
**** Describes desired infrastructure
**** Example
***** 3 cloud VMs
***** PostgreSQL database
***** 100 GB storage
***** Ports 80 & 443
*** Terraform
**** IaC Tool by HashiCorp
**** Uses HCL configuration files
**** Works with cloud / infrastructure providers
**** Workflow
***** Write configuration
***** Initialize - terraform init
***** Preview changes - terraform plan
***** Apply changes - terraform apply
***** Destroy resources - terraform destroy
**** Key Capabilities
***** State Management
****** Tracks managed resources
****** Helps avoid duplicate creation
***** Execution Plan
****** Previews proposed changes
***** Dependency Graph
****** Orders dependent resources
****** Avoids arbitrary sleep timers
***** Drift Detection
****** Detects differences from configuration
****** Refresh / plan reveals many changes
***** Multi-Cloud
****** Common workflow across providers
**** Git Integration
***** Version control
***** Review & collaboration

** 3. Containers
*** Problem
**** Software works in development
**** Fails on another server
***** Missing libraries
***** Different runtime versions
***** OS / configuration differences
*** Container Image
**** Packages application & dependencies
**** Libraries, runtime & configuration
**** Used to create containers
*** Container
**** Running instance of an image
**** Isolated application environment
**** Shares host OS kernel
*** Docker
**** Builds images
**** Runs containers
*** Virtual Machine vs Container
**** VM has its own guest OS
**** Container shares host kernel
**** Hypervisor manages VMs
**** Container runtime runs containers

** 4. Kubernetes (K8s)
*** Definition
**** Orchestrates containerized applications
**** Across multiple servers
**** Maintains desired workload state
*** Kubernetes Cluster
**** Group of networked nodes
**** Nodes may be physical or virtual
**** Created / provisioned using infrastructure tools
*** Control Plane
**** Manages cluster state
**** Schedules workloads
**** Coordinates controllers
*** Worker Nodes
**** Run application workloads
**** Have container runtime
**** Managed by the control plane
*** Core Resource Hierarchy
**** Cluster
***** Node = server
****** Pod = smallest deployable unit
******* Container = application process
*** Desired State
**** YAML manifests describe resources
**** Kubernetes controllers reconcile actual state
**** Failed Pods may be replaced
**** Replacement Pods may have different IPs

** 5. Inner IaC - Kubernetes Manifests
*** Definition
**** Defines workloads & cluster resources
**** Applied through Kubernetes API
*** YAML
**** Human-readable configuration format
**** File extension .yaml / .yml
**** Not a PDF, XML or JSON file
*** Common Manifest Structure
**** apiVersion
***** Kubernetes API version
**** kind
***** Resource type
**** metadata
***** name
***** labels
**** spec
***** Desired configuration
*** Labels & Selectors
**** Labels
***** Key-value metadata on objects
***** Example: app = payment
**** Selectors
***** Find matching objects by labels
***** Connect Services to Pods
*** Deployment
**** Manages stateless application replicas
**** Creates / manages ReplicaSets
**** Maintains desired Pod count
**** Supports rolling updates & rollbacks
**** Replaces failed Pods through controllers
**** Example
***** payment-service
***** 3 desired replicas
*** Service
**** Stable virtual IP & DNS name
**** Targets Pods using selectors
**** Distributes traffic to eligible endpoints
**** Decouples clients from Pod IP changes
**** Example
***** payment-service
***** Port 8080
*** HPA - Horizontal Pod Autoscaler
**** Adjusts replica count dynamically
**** Targets a Deployment or other scalable resource
**** Uses CPU / memory / custom metrics
**** Requires suitable metrics support
**** Example
***** Minimum replicas = 1
***** Maximum replicas = 5
***** Scales according to measured load
*** PDB - Pod Disruption Budget
**** Limits simultaneous voluntary disruptions
**** Protects workload availability
**** Relevant to supported maintenance / eviction
**** Does not prevent every Pod failure
**** Does not replace Deployment rolling-update settings
*** Helm
**** Kubernetes package manager
**** Charts contain templates & values
**** Generates Kubernetes manifests
**** Installs / upgrades / rolls back releases

** 6. Operational Flow
*** 1. Provision infrastructure
**** Terraform creates VMs, networks & storage
**** Provision Kubernetes cluster
*** 2. Package application
**** Build container image
**** Store image in a registry
*** 3. Declare workload
**** Helm chart or Kubernetes YAML
**** Deployment, Service, HPA, PDB
*** 4. Apply configuration
**** Kubernetes API accepts resources
**** Controllers reconcile desired state
*** 5. Run & maintain application
**** Scheduler places Pods on nodes
**** Service routes traffic to Pods
**** HPA adjusts replica count
**** PDB protects against excessive voluntary evictions
**** Deployment manages application rollouts
@endmindmap

