-- +goose Up
-- +goose StatementBegin

-- Juniper topology-based questions for all exams
-- Generated 90 questions

-- Ensure topology question type exists
ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_question_type_check;
ALTER TABLE questions ADD CONSTRAINT questions_question_type_check
  CHECK (question_type IN ('single-choice', 'multiple-choice', 'drag-drop', 'fill-blank', 'simlet', 'topology'));

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('ceaf0c7d-b087-553c-a5af-0f7ad61e804e', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Refer to the topology:

      [R1] ge-0/0/0 --- ge-0/0/0 [R2]
      10.1.12.0/24

R1's ge-0/0/0 has IP 10.1.12.1/24. R2's ge-0/0/0 has IP 10.1.12.2/24.
A ping from R1 to 10.1.12.2 succeeds. Which route appears in R1's routing table?$$::text, $$[{"id": "A", "text": "10.1.12.0/24 via ge-0/0/0.0", "is_correct": true}, {"id": "B", "text": "10.1.12.2/32 via ge-0/0/0.0", "is_correct": false}, {"id": "C", "text": "0.0.0.0/0 via 10.1.12.2", "is_correct": false}, {"id": "D", "text": "No route; directly connected hosts do not need routes", "is_correct": false}]$$::jsonb, $$A directly connected network route is installed for 10.1.12.0/24 when the interface is configured.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$Routing Fundamentals$$::text, 20.0, '546eed178a3140f5', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('ac467ceb-1a25-55f0-9c5f-911d6c0ce1ae', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'troubleshoot', $$Topology:

   [PC1]---ge-0/0/1 [R1] ge-0/0/2---[PC2]
   192.168.1.0/24    192.168.2.0/24

R1 has no static routes. PC1 can reach R1's ge-0/0/1 but not PC2. What is missing?$$::text, $$[{"id": "A", "text": "A default route on PC1", "is_correct": false}, {"id": "B", "text": "A routing protocol on R1", "is_correct": false}, {"id": "C", "text": "Static routes or default gateways on PCs", "is_correct": true}, {"id": "D", "text": "A firewall policy", "is_correct": false}]$$::jsonb, $$Each subnet is directly connected to R1, but PCs need a default gateway pointing to R1 to reach other subnets.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$Routing Fundamentals$$::text, 20.0, '421e2f3085a08b03', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('187f1f64-9176-5479-ab0c-ee836aa35899', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$Refer to the topology:

   [R1]---[R2]---[R3]
   Area 0   Area 1

R1 is in Area 0, R2 is an ABR, R3 is in Area 1. R3 advertises 10.3.3.0/24.
What LSA type does R1 see for 10.3.3.0/24?$$::text, $$[{"id": "A", "text": "Type 1", "is_correct": false}, {"id": "B", "text": "Type 2", "is_correct": false}, {"id": "C", "text": "Type 3", "is_correct": true}, {"id": "D", "text": "Type 5", "is_correct": false}]$$::jsonb, $$Inter-area routes are advertised as Type 3 Summary LSAs by ABRs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$OSPF$$::text, 20.0, 'e8f37f2ec2e64f31', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('ce4ec3d4-60a2-5bd5-839d-1d4819596455', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'troubleshoot', $$Topology:

   [R1]---ge-0/0/0   ge-0/0/0---[R2]
   10.10.10.1/30      10.10.10.2/30

Both interfaces are up but OSPF adjacency is stuck at 2-Way. What is the most likely cause?$$::text, $$[{"id": "A", "text": "MTU mismatch", "is_correct": false}, {"id": "B", "text": "Network type broadcast with no DR election on point-to-point", "is_correct": true}, {"id": "C", "text": "Area ID mismatch", "is_correct": false}, {"id": "D", "text": "Authentication mismatch", "is_correct": false}]$$::jsonb, $$On a point-to-point link OSPF should use point-to-point network type to avoid 2-Way state.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$OSPF$$::text, 20.0, 'eb0f7cb8918c227c', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('278ef756-63ba-5a33-8b5d-34b1ec30454b', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$Refer to the topology:

   [SW1]---[SW2]---[SW3]
   All links are trunk

SW1 is the root bridge. Which ports on SW2 are in a forwarding state?$$::text, $$[{"id": "A", "text": "Only the port toward SW1", "is_correct": false}, {"id": "B", "text": "The port toward SW1 and one port toward SW3", "is_correct": true}, {"id": "C", "text": "All ports", "is_correct": false}, {"id": "D", "text": "No ports", "is_correct": false}]$$::jsonb, $$Root port faces root; one designated port forwards per segment. The other port is blocked.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$Layer 2$$::text, 20.0, '93ee05136b896dac', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('eb0a1825-2988-5133-b067-77be07bf6c46', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Topology:

   [R1]---[R2]---[R3]
   eBGP   iBGP

R2 is a route reflector. R1 and R3 are clients. R1 advertises a route. How does R3 receive it?$$::text, $$[{"id": "A", "text": "Directly from R1 via eBGP", "is_correct": false}, {"id": "B", "text": "Reflected by R2", "is_correct": true}, {"id": "C", "text": "Via OSPF", "is_correct": false}, {"id": "D", "text": "It does not receive it", "is_correct": false}]$$::jsonb, $$Route reflectors reflect routes between iBGP clients.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$BGP$$::text, 20.0, '530fba382e4fd02f', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('2062be02-129b-5ab3-bb16-e737a0e3b71d', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Refer to the topology:

   [Host]---ge-0/0/1 [R1] ge-0/0/2---[Internet]

A source NAT rule is configured on R1 for the Host subnet. Which address does the Internet see?$$::text, $$[{"id": "A", "text": "Host private IP", "is_correct": false}, {"id": "B", "text": "R1 ge-0/0/2 public IP", "is_correct": true}, {"id": "C", "text": "R1 ge-0/0/1 IP", "is_correct": false}, {"id": "D", "text": "No address; NAT breaks the connection", "is_correct": false}]$$::jsonb, $$Source NAT translates private source addresses to the public address on the egress interface.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$NAT$$::text, 20.0, '9d528c9a1f324249', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('37169723-55ca-5dd5-a7a4-a5c0ed9372f1', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'understand', $$Refer to the MPLS topology:

   CE1--PE1--P--PE2--CE2

Which device assigns the VPN label for CE2's routes?$$::text, $$[{"id": "A", "text": "P", "is_correct": false}, {"id": "B", "text": "PE1", "is_correct": false}, {"id": "C", "text": "PE2", "is_correct": true}, {"id": "D", "text": "CE2", "is_correct": false}]$$::jsonb, $$The egress PE assigns the VPN label for routes advertised to other PEs via MP-BGP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$MPLS L3VPN$$::text, 25.0, '2f3be299564b83aa', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('416fb4f0-7335-5ff1-883d-7f3919462c41', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Topology:

   [R1]---[R2]---[R3]
   LDP enabled on all links

Which statement about LDP adjacencies is true?$$::text, $$[{"id": "A", "text": "LDP sessions are TCP-based between directly connected neighbors", "is_correct": true}, {"id": "B", "text": "LDP uses UDP only", "is_correct": false}, {"id": "C", "text": "LDP requires RSVP", "is_correct": false}, {"id": "D", "text": "LDP labels are only for BGP routes", "is_correct": false}]$$::jsonb, $$LDP discovery uses UDP Hellos, but the session is TCP-based between neighbors.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$MPLS$$::text, 25.0, '9aa348440cd8ae0a', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('74e45916-5914-54e7-854b-72da1e32daa5', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Refer to the topology:

   [AS 65001]---[AS 65002]---[AS 65003]

AS 65002 receives the same prefix from both neighbors. Which attribute influences inbound traffic?$$::text, $$[{"id": "A", "text": "Local Preference", "is_correct": false}, {"id": "B", "text": "MED", "is_correct": true}, {"id": "C", "text": "Origin", "is_correct": false}, {"id": "D", "text": "Next Hop", "is_correct": false}]$$::jsonb, $$MED is advertised to external peers and influences how they send traffic into your AS.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$BGP$$::text, 25.0, 'b7e327de96104dca', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('beaa524b-bd93-5c50-884b-07a8a043b4c4', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'analyze', $$Topology:

   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]

All routers are L1/L2. How does R3 learn R1's L1 routes?$$::text, $$[{"id": "A", "text": "R2 leaks them into L2", "is_correct": true}, {"id": "B", "text": "They are flooded natively", "is_correct": false}, {"id": "C", "text": "Via L1/L2 adjacency only", "is_correct": false}, {"id": "D", "text": "They are not reachable", "is_correct": false}]$$::jsonb, $$L1/L2 routers leak L1 routes into the L2 backbone.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$IS-IS$$::text, 25.0, '5e02ff4e7550afd7', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('0a6a45bc-5020-5957-a369-c4127041cca4', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Refer to the RSVP-TE topology:

   [R1]---[R2]---[R3]---[R4]

All links are 10 Gbps. An LSP from R1 to R4 requires 5 Gbps. What does CSPF do?$$::text, $$[{"id": "A", "text": "Chooses the path with lowest IGP metric", "is_correct": false}, {"id": "B", "text": "Chooses any path that satisfies bandwidth", "is_correct": true}, {"id": "C", "text": "Ignores bandwidth", "is_correct": false}, {"id": "D", "text": "Rejects the LSP", "is_correct": false}]$$::jsonb, $$CSPF selects a path that satisfies constraints such as bandwidth.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"}$$::text[], $$MPLS TE$$::text, 25.0, '04025e04aabb41b8', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a56f333d-3637-5a75-915c-5c184ce42c13', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'topology', 1, 'understand', $$Refer to the SRX topology:

   [Untrust]---[SRX]---[Trust]---[Server]
                |
             [DMZ]---[Web]

A security policy allows HTTP from Untrust to DMZ. Which zone is the source?$$::text, $$[{"id": "A", "text": "Trust", "is_correct": false}, {"id": "B", "text": "DMZ", "is_correct": false}, {"id": "C", "text": "Untrust", "is_correct": true}, {"id": "D", "text": "Server", "is_correct": false}]$$::jsonb, $$The source zone in a security policy is where the traffic originates.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"}$$::text[], $$Zones$$::text, 25.0, '71438ddf71b9ecce', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('2bea8f92-81dc-596b-86d2-4457c70773c4', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Topology:

   [Host-A]---[SRX]---[Host-B]
   10.1.1.0/24      203.0.113.0/24

Host-A initiates a session to Host-B. Which NAT type translates Host-A's source address?$$::text, $$[{"id": "A", "text": "Static NAT", "is_correct": false}, {"id": "B", "text": "Destination NAT", "is_correct": false}, {"id": "C", "text": "Source NAT", "is_correct": true}, {"id": "D", "text": "Proxy ARP", "is_correct": false}]$$::jsonb, $$Source NAT translates the source IP address of outgoing traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"}$$::text[], $$NAT$$::text, 25.0, '18676c4460163793', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e96a9e8e-7ddd-5cb3-b5a5-7af3d633da31', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Refer to the topology:

   [Internet]---[SRX-1]====[SRX-2]---[Trust]
                    Control Link   Data Link

What is the purpose of the data link in a chassis cluster?$$::text, $$[{"id": "A", "text": "State synchronization", "is_correct": false}, {"id": "B", "text": "Forwarding traffic between nodes", "is_correct": true}, {"id": "C", "text": "Configuration management", "is_correct": false}, {"id": "D", "text": "Out-of-band management", "is_correct": false}]$$::jsonb, $$The data/fabric link carries forwarded traffic between chassis cluster nodes.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"}$$::text[], $$High Availability$$::text, 25.0, '632549f2bbe103a7', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('6e1fee8a-1a6a-5e71-b5f8-f9aa6a3b47a2', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Topology:

   [User]---[SRX]---[Web]

A Screen option blocks a host that opens many TCP connections to many destination ports. Which option is it?$$::text, $$[{"id": "A", "text": "SYN flood", "is_correct": false}, {"id": "B", "text": "Port scan", "is_correct": true}, {"id": "C", "text": "IP spoofing", "is_correct": false}, {"id": "D", "text": "Session limit", "is_correct": false}]$$::jsonb, $$The port scan Screen option detects hosts scanning many destination ports.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"}$$::text[], $$Screens$$::text, 25.0, 'b49aa3a428a5341e', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e9a2d356-a127-55e8-bd36-3615067db6f7', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Refer to the topology:

   [Branch]---VPN---[HQ]
   10.1.0.0/16     10.2.0.0/16

A route-based IPsec VPN is configured. What must exist for traffic to flow?$$::text, $$[{"id": "A", "text": "Proxy-ID matching all traffic", "is_correct": false}, {"id": "B", "text": "Routes pointing to the VPN tunnel interface", "is_correct": true}, {"id": "C", "text": "A security policy from Branch to Branch", "is_correct": false}, {"id": "D", "text": "NAT on both sides", "is_correct": false}]$$::jsonb, $$Route-based VPNs require routes to direct traffic into the tunnel interface.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"}$$::text[], $$VPN$$::text, 25.0, '4c21554c5e80a390', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a5f163d6-d08d-59a9-bdfa-44ad109efe89', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the EVPN-VXLAN topology:

   [Leaf1]====[Spine]====[Leaf2]
   VTEP       VTEP?       VTEP

Which device is typically NOT a VTEP in a two-tier EVPN-VXLAN fabric?$$::text, $$[{"id": "A", "text": "Leaf switch", "is_correct": false}, {"id": "B", "text": "Spine switch", "is_correct": true}, {"id": "C", "text": "Border leaf", "is_correct": false}, {"id": "D", "text": "Hypervisor", "is_correct": false}]$$::jsonb, $$Spine switches provide IP underlay; leaf switches act as VTEPs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"}$$::text[], $$VXLAN$$::text, 25.0, 'a856634172e80b97', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e8d4bd26-8b6a-5967-a793-fc945a0ad808', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [Server1]---[Leaf1]====[Leaf2]---[Server2]
   VNI 10001             VNI 10001

What identifies the Layer 2 segment that Server1 and Server2 share?$$::text, $$[{"id": "A", "text": "VLAN ID", "is_correct": false}, {"id": "B", "text": "VNI", "is_correct": true}, {"id": "C", "text": "Route Distinguisher", "is_correct": false}, {"id": "D", "text": "Loopback IP", "is_correct": false}]$$::jsonb, $$VXLAN Network Identifier (VNI) identifies the Layer 2 overlay segment.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"}$$::text[], $$VXLAN$$::text, 25.0, 'dac12d605b66f7c6', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('47f7c09b-4e76-5b7d-b872-e11d1553d7be', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004', 'topology', 3, 'understand', $$Refer to the topology:

   [Server]---[Leaf1]====[Leaf2]---[Server]
            ES-1         ES-1

Both leaf switches are connected to the same server. What provides active-active multihoming?$$::text, $$[{"id": "A", "text": "MC-LAG", "is_correct": false}, {"id": "B", "text": "EVPN multihoming", "is_correct": true}, {"id": "C", "text": "VRRP", "is_correct": false}, {"id": "D", "text": "LACP", "is_correct": false}]$$::jsonb, $$EVPN multihoming via Ethernet Segments provides active-active L2 multihoming.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"}$$::text[], $$EVPN$$::text, 25.0, '6cf7e6252805a5d2', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a63cbb42-9150-589a-945d-f016b19ef16a', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [SW1]====[SW2]====[SW3]
   Member   Member   Member

What technology combines these switches into one logical control plane?$$::text, $$[{"id": "A", "text": "MC-LAG", "is_correct": false}, {"id": "B", "text": "Virtual Chassis", "is_correct": true}, {"id": "C", "text": "EVPN", "is_correct": false}, {"id": "D", "text": "VCF", "is_correct": false}]$$::jsonb, $$Virtual Chassis combines multiple switches into a single logical device.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"}$$::text[], $$Virtual Chassis$$::text, 25.0, '09275116959e9209', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a9509689-36ce-53f7-87a8-7a71fc481627', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the topology:

   [Compute]---[vRouter]---[Underlay]---[vRouter]---[Compute]

Which Contrail component runs on the compute node?$$::text, $$[{"id": "A", "text": "Config node", "is_correct": false}, {"id": "B", "text": "vRouter", "is_correct": true}, {"id": "C", "text": "Control node", "is_correct": false}, {"id": "D", "text": "Analytics node", "is_correct": false}]$$::jsonb, $$Contrail vRouter runs on compute nodes and forwards tenant traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"}$$::text[], $$Contrail$$::text, 25.0, '9f994015db366451', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('d6d697e4-1a2f-5573-90ce-2c85aa9f9059', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005', 'topology', 1, 'remember', $$Refer to the automation topology:

   [Ansible]---NETCONF/SSH---[Junos]

Which Ansible module is used to push configuration to Junos?$$::text, $$[{"id": "A", "text": "ios_config", "is_correct": false}, {"id": "B", "text": "junos_config", "is_correct": true}, {"id": "C", "text": "netconf_rpc", "is_correct": false}, {"id": "D", "text": "template", "is_correct": false}]$$::jsonb, $$The junos_config module manages Junos configurations via NETCONF.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"}$$::text[], $$Ansible$$::text, 25.0, '4bdf6dc59592648b', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('c3c42f9c-4089-5a9b-847f-6bc2adff1c3b', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005', 'topology', 1, 'remember', $$Topology:

   [Python]---NETCONF-830---[Junos]

Which Python library is commonly used for this connection?$$::text, $$[{"id": "A", "text": "Paramiko", "is_correct": false}, {"id": "B", "text": "ncclient", "is_correct": true}, {"id": "C", "text": "Requests", "is_correct": false}, {"id": "D", "text": "Scapy", "is_correct": false}]$$::jsonb, $$ncclient is the standard Python NETCONF client library.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"}$$::text[], $$NETCONF$$::text, 25.0, 'c82c4ae3cc8126af', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('98965450-8653-592a-8a8c-679e2e1398db', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [Salt Master]---[Proxy Minion]---[Junos]

Why is a proxy minion used?$$::text, $$[{"id": "A", "text": "Junos cannot run a native minion", "is_correct": true}, {"id": "B", "text": "It replaces the master", "is_correct": false}, {"id": "C", "text": "It is faster than a regular minion", "is_correct": false}, {"id": "D", "text": "Junos does not support Salt", "is_correct": false}]$$::jsonb, $$Junos devices use Salt proxy minions because they cannot run a native minion.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"}$$::text[], $$SaltStack$$::text, 25.0, 'b3139766cef32b16', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('0549c95c-885b-501b-9804-76bbc45b360c', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Topology:

   [Client]---HTTP---[Junos REST API]

Which HTTP method replaces a complete resource?$$::text, $$[{"id": "A", "text": "POST", "is_correct": false}, {"id": "B", "text": "PUT", "is_correct": true}, {"id": "C", "text": "PATCH", "is_correct": false}, {"id": "D", "text": "GET", "is_correct": false}]$$::jsonb, $$PUT replaces the entire resource, while PATCH applies partial updates.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"}$$::text[], $$REST API$$::text, 25.0, 'dd15624655772b9e', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('acdfab8a-8390-5ade-8d9c-162506daf943', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [Junos]--->[SYSLOG]--->[ collector ]

Which on-box script type can parse syslog events and take action?$$::text, $$[{"id": "A", "text": "Op script", "is_correct": false}, {"id": "B", "text": "Event script", "is_correct": true}, {"id": "C", "text": "Commit script", "is_correct": false}, {"id": "D", "text": "SNMP script", "is_correct": false}]$$::jsonb, $$Event scripts are triggered by syslog events and can take corrective actions.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"}$$::text[], $$Junos Automation$$::text, 25.0, 'f020e919562f4092', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('70bbba1e-effe-598a-be55-a5ce0ae6346d', 'b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007', 'topology', 2, 'understand', $$Refer to the cloud topology:

   [VPC-A]---[Contrail]---[VPC-B]

Which protocol provides the overlay between VPCs?$$::text, $$[{"id": "A", "text": "MPLS", "is_correct": false}, {"id": "B", "text": "VXLAN", "is_correct": true}, {"id": "C", "text": "L2TP", "is_correct": false}, {"id": "D", "text": "PPPoE", "is_correct": false}]$$::jsonb, $$VXLAN is commonly used as the overlay encapsulation in cloud fabrics.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"}$$::text[], $$Overlay Networking$$::text, 25.0, '28f22c1753ff3814', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('69a1793f-4684-5c51-90a7-ba723c415930', 'b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007', 'topology', 2, 'understand', $$Topology:

   [Tenant-A]---[vRouter]---[Underlay]---[vRouter]---[Tenant-B]

Which component routes tenant traffic on the compute node?$$::text, $$[{"id": "A", "text": "Config node", "is_correct": false}, {"id": "B", "text": "vRouter", "is_correct": true}, {"id": "C", "text": "Control node", "is_correct": false}, {"id": "D", "text": "Analytics node", "is_correct": false}]$$::jsonb, $$Contrail vRouter runs on compute nodes and forwards tenant traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"}$$::text[], $$Contrail$$::text, 25.0, 'b1f942ecdaaefb95', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('03e18d7d-cc47-5117-b425-a4235a2255a2', 'b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007', 'topology', 2, 'understand', $$Refer to the topology:

   [On-prem DC]---WAN---[Public Cloud IaaS]
   10.0.0.0/16          172.16.0.0/16

What is required for VMs in both locations to communicate privately?$$::text, $$[{"id": "A", "text": "NAT overload", "is_correct": false}, {"id": "B", "text": "IPsec/SD-WAN VPN", "is_correct": true}, {"id": "C", "text": "Public IP on every VM", "is_correct": false}, {"id": "D", "text": "Direct physical connection", "is_correct": false}]$$::jsonb, $$A VPN or SD-WAN overlay connects private addresses across public networks.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"}$$::text[], $$Cloud Connectivity$$::text, 25.0, '6ea79b115274e5aa', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('beec1ea4-cb8e-5b9d-a4ab-eecc24fd934b', 'b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007', 'topology', 1, 'understand', $$Topology:

   [Users]---[SaaS App]---[Provider Data Center]

Which cloud service model is shown?$$::text, $$[{"id": "A", "text": "IaaS", "is_correct": false}, {"id": "B", "text": "PaaS", "is_correct": false}, {"id": "C", "text": "SaaS", "is_correct": true}, {"id": "D", "text": "DaaS", "is_correct": false}]$$::jsonb, $$SaaS delivers complete applications to end users.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"}$$::text[], $$Cloud Service Models$$::text, 25.0, '9bd95e16414ca6d8', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('beb3706e-fb52-580d-a319-7196d8f88659', 'b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007', 'topology', 2, 'understand', $$Refer to the topology:

   [Bare-metal]---[Hypervisor]---[VMs]---[Containers]

What does NFV enable in this stack?$$::text, $$[{"id": "A", "text": "Virtualized network functions such as routers and firewalls", "is_correct": true}, {"id": "B", "text": "Physical cabling automation", "is_correct": false}, {"id": "C", "text": "Replacement of hypervisors", "is_correct": false}, {"id": "D", "text": "Bare-metal OS installation", "is_correct": false}]$$::jsonb, $$NFV virtualizes network functions that traditionally ran on dedicated hardware.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"}$$::text[], $$NFV$$::text, 25.0, 'f04334625fb9ba4e', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('35d48a1e-3970-5808-9626-0cef93a4039d', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$Refer to the BGP topology:

   AS 65001 --- eBGP --- AS 65002 --- eBGP --- AS 65003

AS 65002 receives a route from AS 65001 with Local Preference 200 and MED 50.
The same route is received from AS 65003 with Local Preference 100 and MED 10.
Which path does AS 65002 prefer?$$::text, $$[{"id": "A", "text": "Path through AS 65001", "is_correct": true}, {"id": "B", "text": "Path through AS 65003", "is_correct": false}, {"id": "C", "text": "Load-balance", "is_correct": false}, {"id": "D", "text": "Cannot decide", "is_correct": false}]$$::jsonb, $$Local Preference is evaluated before MED. Higher LP wins.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$BGP$$::text, 20.0, '1e384ac3b36a9ed8', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a5b5bae0-323a-54e7-9a11-80348399940a', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Topology:

   [SW1]---[SW2]---[SW3] (triangle)

Bridge IDs: SW1=4096.00:00:00:00:00:01, SW2=32768...02, SW3=32768...03.
Which switch is root?$$::text, $$[{"id": "A", "text": "SW1", "is_correct": true}, {"id": "B", "text": "SW2", "is_correct": false}, {"id": "C", "text": "SW3", "is_correct": false}, {"id": "D", "text": "Cannot determine", "is_correct": false}]$$::jsonb, $$Lowest bridge ID wins root election.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$Layer 2$$::text, 20.0, '18ca9cba0d924a64', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('b40a6c21-7641-5843-8e10-990fd8d60ab4', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Refer to the CoS topology:

   [Voice]---[EF Queue]---[Router]---[Best-Effort Queue]---[Data]

Which scheduler treats the EF queue first?$$::text, $$[{"id": "A", "text": "Strict-high priority", "is_correct": true}, {"id": "B", "text": "WRR", "is_correct": false}, {"id": "C", "text": "RED", "is_correct": false}, {"id": "D", "text": "Tail drop", "is_correct": false}]$$::jsonb, $$Strict-high priority queues are serviced before other queues.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$CoS$$::text, 15.0, '3efc6003581d2526', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('45320141-627b-5abb-89af-277cb265baa3', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$Topology:

   [R1]---Area 0---[R2]---Area 1---[R3]

R1 advertises 10.1.1.0/24. What LSA type does R3 see?$$::text, $$[{"id": "A", "text": "Type 1", "is_correct": false}, {"id": "B", "text": "Type 2", "is_correct": false}, {"id": "C", "text": "Type 3", "is_correct": true}, {"id": "D", "text": "Type 5", "is_correct": false}]$$::jsonb, $$Inter-area routes are Type 3 Summary LSAs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$OSPF$$::text, 20.0, 'f9975566fefa55f1', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a7481394-441a-5238-84c1-93d4f8db9458', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$Refer to the EVPN-VXLAN campus topology:

   [Leaf1]====[Spine1]====[Leaf2]
   VTEP                  VTEP

Which device role typically is NOT a VTEP?$$::text, $$[{"id": "A", "text": "Access leaf", "is_correct": false}, {"id": "B", "text": "Spine", "is_correct": true}, {"id": "C", "text": "WAN edge", "is_correct": false}, {"id": "D", "text": "Core", "is_correct": false}]$$::jsonb, $$Spine provides IP underlay only; leaves are VTEPs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$EVPN/VXLAN$$::text, 20.0, '85c20175d9d41227', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('4dde0a19-601a-59fc-b080-8359d34187ce', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$Topology:

   [PE1]---[P]---[PE2]
   VPN-A     VPN-A

Which protocol carries VPNv4 routes between PE1 and PE2?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "LDP", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "RSVP", "is_correct": false}]$$::jsonb, $$MP-BGP with VPNv4 address family exchanges customer routes between PEs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$BGP/MPLS$$::text, 15.0, 'f2731ed188698bc3', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('bd3dc83c-8e97-501f-bfd0-f81f6b5fca92', 'b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$Refer to the multicast topology:

   [Source]---[R1]---[R2]---[Receiver]
              RP

Which tree is initially built from source to RP in PIM-SM?$$::text, $$[{"id": "A", "text": "Shared tree (*,G)", "is_correct": false}, {"id": "B", "text": "Shortest-path tree (S,G)", "is_correct": true}, {"id": "C", "text": "Bidirectional tree", "is_correct": false}, {"id": "D", "text": "None", "is_correct": false}]$$::jsonb, $$Source registers with RP and an SPT (S,G) is built from source to RP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"}$$::text[], $$Multicast$$::text, 10.0, '1a8f72a4b6e34bdd', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('02f3c731-e82d-5150-96d6-8574ed1d9638', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Refer to the MPLS L3VPN topology:

   CE1--PE1--P--PE2--CE2
   VPN-A        VPN-A

Which protocol carries VPNv4 routes between PE1 and PE2?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "LDP", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "RSVP", "is_correct": false}]$$::jsonb, $$MP-BGP with VPNv4 address family exchanges customer routes between PE routers.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$MPLS L3VPN$$::text, 25.0, 'bc189999fbcdb25a', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('225d24fe-2d9a-54c3-be88-826080bf2357', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'analyze', $$Topology:

   [R1]---[R2]---[R3]---[R4]
   All 10 Gbps except R2-R3 1 Gbps

An LSP from R1 to R4 needs 5 Gbps. Which path does CSPF choose?$$::text, $$[{"id": "A", "text": "R1-R2-R3-R4", "is_correct": false}, {"id": "B", "text": "Any path satisfying bandwidth", "is_correct": true}, {"id": "C", "text": "Lowest IGP metric path", "is_correct": false}, {"id": "D", "text": "CSPF ignores bandwidth", "is_correct": false}]$$::jsonb, $$CSPF selects a path that meets bandwidth constraints.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$MPLS TE$$::text, 20.0, 'bde6393e92840abc', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('d238de0a-fe5d-50ae-b5f7-6a4c91d2c18a', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Refer to the BGP route reflector topology:

         [RR]
        /    \
     [PE1]  [PE2]

PE1 receives a VPNv4 route from a CE. How does PE2 learn it?$$::text, $$[{"id": "A", "text": "Directly from PE1", "is_correct": false}, {"id": "B", "text": "Reflected by RR", "is_correct": true}, {"id": "C", "text": "Via OSPF", "is_correct": false}, {"id": "D", "text": "Via LDP", "is_correct": false}]$$::jsonb, $$Route reflectors reflect routes between iBGP clients.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$BGP$$::text, 20.0, '7b5dc38c924f9560', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('4335c6dc-9f33-5bec-882d-ea782cc86d6e', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'understand', $$Topology:

   [R1]---[R2]---[R3]
   SRGB 1000-2000 all nodes

R1 sends traffic using explicit path 1002-1003. What does 1003 represent?$$::text, $$[{"id": "A", "text": "R3's prefix SID", "is_correct": true}, {"id": "B", "text": "R2's adjacency SID", "is_correct": false}, {"id": "C", "text": "R1's node SID", "is_correct": false}, {"id": "D", "text": "Service label", "is_correct": false}]$$::jsonb, $$1003 is the prefix/node SID for R3 within the SRGB.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$Segment Routing$$::text, 15.0, 'd45c3299b1adf7cf', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('571535f9-c8fa-57e8-8b49-63a2c1fb1766', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'analyze', $$Refer to the IS-IS topology:

   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]

All routers are L1/L2. Which statement is true?$$::text, $$[{"id": "A", "text": "R3 sees R1's L1 routes natively", "is_correct": false}, {"id": "B", "text": "R2 leaks L1 routes from Area 49.0001 into L2", "is_correct": true}, {"id": "C", "text": "IS-IS does not support route leaking", "is_correct": false}, {"id": "D", "text": "R3 must be L1 only", "is_correct": false}]$$::jsonb, $$L1/L2 routers leak L1 routes into the L2 backbone.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$IS-IS$$::text, 15.0, '66f7947b0af3237d', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('5613e5fd-3e84-5d4b-99f2-c64a9318b97d', 'b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$Topology:

   [R1]---[R2]---[R3]
   LDP enabled

Which transport does LDP use for session establishment?$$::text, $$[{"id": "A", "text": "UDP only", "is_correct": false}, {"id": "B", "text": "TCP", "is_correct": true}, {"id": "C", "text": "SCTP", "is_correct": false}, {"id": "D", "text": "ICMP", "is_correct": false}]$$::jsonb, $$LDP discovery uses UDP, but the session is TCP-based.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"}$$::text[], $$MPLS$$::text, 15.0, '188390645ddc48e4', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('937a1906-ebc0-5751-87ab-137239c26630', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Refer to the SRX topology:

   [Untrust]---[SRX]---[Trust]
                |
             [DMZ]

A policy allows HTTP from Untrust to DMZ. What is the destination zone?$$::text, $$[{"id": "A", "text": "Untrust", "is_correct": false}, {"id": "B", "text": "Trust", "is_correct": false}, {"id": "C", "text": "DMZ", "is_correct": true}, {"id": "D", "text": "Any", "is_correct": false}]$$::jsonb, $$The destination zone is where the target resource resides.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$Security Policies$$::text, 20.0, '776e453c159e4fa5', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('66f2efdd-d323-5cfd-9d3c-d7bc6d930951', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Topology:

   [Branch]---VPN---[HQ]
   10.1.0.0/16     10.2.0.0/16

What is required for route-based VPN traffic?$$::text, $$[{"id": "A", "text": "Proxy-ID", "is_correct": false}, {"id": "B", "text": "Routes to tunnel interface", "is_correct": true}, {"id": "C", "text": "NAT on both sides", "is_correct": false}, {"id": "D", "text": "Same subnet", "is_correct": false}]$$::jsonb, $$Route-based VPNs require routes to direct traffic into the tunnel.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$VPN$$::text, 20.0, '3520060b779a5645', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('100e52f7-b53c-5b76-884f-86a20006a3f9', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Refer to the topology:

   [User]---[SRX]---[Web]

AppSecure identifies HTTPS traffic as a specific application. Which Layer does AppID inspect?$$::text, $$[{"id": "A", "text": "Layer 3", "is_correct": false}, {"id": "B", "text": "Layer 4", "is_correct": false}, {"id": "C", "text": "Layer 7", "is_correct": true}, {"id": "D", "text": "Layer 2", "is_correct": false}]$$::jsonb, $$AppID performs Layer 7 inspection to identify applications.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$AppSecure$$::text, 20.0, 'efd94c26402f63fa', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('0eca24dc-ef09-5537-99ec-9b296be16ead', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Topology:

   [Internet]---[SRX-1]====[SRX-2]---[Trust]

Which link is used for state synchronization in a chassis cluster?$$::text, $$[{"id": "A", "text": "Control link", "is_correct": true}, {"id": "B", "text": "Data link", "is_correct": false}, {"id": "C", "text": "Management", "is_correct": false}, {"id": "D", "text": "Console", "is_correct": false}]$$::jsonb, $$The control link carries state and configuration synchronization.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$High Availability$$::text, 20.0, '3f5b40c452706fcd', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e6652dbe-ceab-5fc7-9261-d0f74fb420c0', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Refer to the topology:

   [Host-A]---[SRX]---[Host-B]
   10.1.1.10      203.0.113.10

Host-A browses to Host-B. Which NAT type translates Host-A's address?$$::text, $$[{"id": "A", "text": "Destination NAT", "is_correct": false}, {"id": "B", "text": "Source NAT", "is_correct": true}, {"id": "C", "text": "Static NAT", "is_correct": false}, {"id": "D", "text": "Twice NAT", "is_correct": false}]$$::jsonb, $$Source NAT translates the source address of outgoing traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$NAT$$::text, 20.0, '642d11c15d01261d', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e5da7d29-544f-5b54-b085-75af7d2136eb', 'b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Topology:

   [Attacker]---[SRX]---[Server]

Many SYN packets hit the Server with no corresponding ACKs. Which Screen option helps?$$::text, $$[{"id": "A", "text": "Port scan", "is_correct": false}, {"id": "B", "text": "SYN flood", "is_correct": true}, {"id": "C", "text": "IP spoofing", "is_correct": false}, {"id": "D", "text": "Session limit", "is_correct": false}]$$::jsonb, $$The SYN flood Screen option detects and mitigates TCP SYN floods.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"}$$::text[], $$Screens$$::text, 20.0, '3cd4f7b989a97988', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('b1f8ecca-ab3b-540a-a79c-3ad15666ea00', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the EVPN topology:

   [Leaf1]====[Spine]====[Leaf2]
   VTEP                  VTEP

Which device role is typically NOT a VTEP?$$::text, $$[{"id": "A", "text": "Leaf", "is_correct": false}, {"id": "B", "text": "Spine", "is_correct": true}, {"id": "C", "text": "Border leaf", "is_correct": false}, {"id": "D", "text": "Hypervisor", "is_correct": false}]$$::jsonb, $$Spine provides IP underlay; leaves act as VTEPs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$VXLAN$$::text, 20.0, '62f06bddbf405550', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('9cea0a3f-66d6-5368-93f7-2e53770568a2', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [Server1]---[Leaf1]====[Leaf2]---[Server2]
   VNI 10001             VNI 10001

What identifies the shared Layer 2 segment?$$::text, $$[{"id": "A", "text": "VLAN", "is_correct": false}, {"id": "B", "text": "VNI", "is_correct": true}, {"id": "C", "text": "RD", "is_correct": false}, {"id": "D", "text": "Loopback", "is_correct": false}]$$::jsonb, $$The VNI identifies the Layer 2 overlay segment.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$VXLAN$$::text, 20.0, '1a6738fcc51b1521', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('667c5ab7-c610-5f55-aba9-d771b0337bba', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 3, 'understand', $$Refer to the topology:

   [Server]---[Leaf1]====[Leaf2]---[Server]
            ES-1         ES-1

What provides active-active multihoming?$$::text, $$[{"id": "A", "text": "MC-LAG", "is_correct": false}, {"id": "B", "text": "EVPN multihoming", "is_correct": true}, {"id": "C", "text": "VRRP", "is_correct": false}, {"id": "D", "text": "LACP", "is_correct": false}]$$::jsonb, $$EVPN multihoming provides active-active L2 multihoming via Ethernet Segments.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$EVPN$$::text, 20.0, '8adf09f8adaef8a7', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('803f1afe-974f-5cc2-aad1-1d8d8fcfe52f', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [SW1]====[SW2]====[SW3]
   Member   Member   Member

What combines them into one logical control plane?$$::text, $$[{"id": "A", "text": "MC-LAG", "is_correct": false}, {"id": "B", "text": "Virtual Chassis", "is_correct": true}, {"id": "C", "text": "EVPN", "is_correct": false}, {"id": "D", "text": "VCF", "is_correct": false}]$$::jsonb, $$Virtual Chassis combines multiple switches into one logical device.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$Virtual Chassis$$::text, 15.0, '541c0366a4eea8fe', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('d0032a6d-1492-5ec6-b0d5-d04895494316', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the topology:

   [Compute]---[vRouter]---[Underlay]---[vRouter]---[Compute]

Which Contrail component runs on the compute node?$$::text, $$[{"id": "A", "text": "Config node", "is_correct": false}, {"id": "B", "text": "vRouter", "is_correct": true}, {"id": "C", "text": "Control node", "is_correct": false}, {"id": "D", "text": "Analytics node", "is_correct": false}]$$::jsonb, $$Contrail vRouter runs on compute nodes and forwards tenant traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$Contrail$$::text, 15.0, '9f994015db366451', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('bd905377-4402-5548-b08b-c2ee1d84e355', 'b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [Spine1]====[Spine2]
      ||        ||
   [Leaf1]====[Leaf2]

Which protocol carries EVPN routes between leaves and spines?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "IS-IS", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "LDP", "is_correct": false}]$$::jsonb, $$EVPN routes are exchanged via MP-BGP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"}$$::text[], $$EVPN$$::text, 15.0, 'b92f7c3aa0dddb7f', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('777b09bd-7b75-597f-9a36-95488b3e68c6', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 1, 'remember', $$Refer to the automation topology:

   [Ansible Control]---NETCONF/SSH---[Junos]

Which module pushes config to Junos?$$::text, $$[{"id": "A", "text": "ios_config", "is_correct": false}, {"id": "B", "text": "junos_config", "is_correct": true}, {"id": "C", "text": "netconf_rpc", "is_correct": false}, {"id": "D", "text": "template", "is_correct": false}]$$::jsonb, $$junos_config manages Junos configurations via NETCONF.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$Ansible$$::text, 20.0, '35a3752fe31aac0d', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('d92c5d5a-dea6-518a-a18b-d62d0a102c61', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 1, 'remember', $$Topology:

   [Python]---NETCONF-830---[Junos]

Which Python library is standard for this?$$::text, $$[{"id": "A", "text": "Paramiko", "is_correct": false}, {"id": "B", "text": "ncclient", "is_correct": true}, {"id": "C", "text": "Requests", "is_correct": false}, {"id": "D", "text": "Scapy", "is_correct": false}]$$::jsonb, $$ncclient is the standard Python NETCONF client library.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$NETCONF$$::text, 20.0, '6758f55e67834228', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('e62cbe41-77ee-5a70-9455-212613ecbe0c', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [NETCONF Client]---RPC---[Junos]---|configuration|\--->[Candidate]

Which operation loads config into the candidate database?$$::text, $$[{"id": "A", "text": "<get-config>", "is_correct": false}, {"id": "B", "text": "<edit-config>", "is_correct": true}, {"id": "C", "text": "<copy-config>", "is_correct": false}, {"id": "D", "text": "<delete-config>", "is_correct": false}]$$::jsonb, $$<edit-config> loads configuration changes into the candidate database.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$NETCONF$$::text, 20.0, 'c6bf120ee1743e31', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('2b943114-8e52-5946-ba7b-9181bcb3136f', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Topology:

   [REST Client]---HTTP---[Junos REST API]

Which method replaces a complete resource?$$::text, $$[{"id": "A", "text": "POST", "is_correct": false}, {"id": "B", "text": "PUT", "is_correct": true}, {"id": "C", "text": "PATCH", "is_correct": false}, {"id": "D", "text": "GET", "is_correct": false}]$$::jsonb, $$PUT replaces the entire resource.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$REST API$$::text, 20.0, 'bd9b35c8a480a36b', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('3d3848a8-8454-5f89-8170-81a06af76016', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [Junos]--->[SYSLOG]--->[Event Script]--->[Action]

Which script type is triggered by syslog events?$$::text, $$[{"id": "A", "text": "Op script", "is_correct": false}, {"id": "B", "text": "Event script", "is_correct": true}, {"id": "C", "text": "Commit script", "is_correct": false}, {"id": "D", "text": "SNMP script", "is_correct": false}]$$::jsonb, $$Event scripts are triggered by syslog events and can take corrective actions.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$Junos Automation$$::text, 20.0, '3d136185112b9016', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('b84c6ba3-fa6f-5268-baef-c3253c6024d4', 'b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Topology:

   [Git]--->[CI/CD]--->[NETCONF]--->[Junos]

What is the benefit of this pipeline?$$::text, $$[{"id": "A", "text": "Version-controlled, automated configuration deployment", "is_correct": true}, {"id": "B", "text": "Faster packet forwarding", "is_correct": false}, {"id": "C", "text": "Physical cabling automation", "is_correct": false}, {"id": "D", "text": "Removes need for routing protocols", "is_correct": false}]$$::jsonb, $$CI/CD with NETCONF enables version-controlled and automated config deployment.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"}$$::text[], $$Automation Concepts$$::text, 20.0, '5fd5a4397f436283', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('445b1adf-089f-533c-9d57-621aa9c81a9d', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$Refer to the BGP topology:

   AS 65001 --- eBGP --- AS 65002 --- eBGP --- AS 65003

AS 65002 receives a route from AS 65001 with Local Preference 200 and MED 50.
The same route is received from AS 65003 with Local Preference 100 and MED 10.
Which path does AS 65002 prefer for outbound traffic?$$::text, $$[{"id": "A", "text": "Path through AS 65001", "is_correct": true}, {"id": "B", "text": "Path through AS 65003", "is_correct": false}, {"id": "C", "text": "It load-balances both paths", "is_correct": false}, {"id": "D", "text": "It cannot decide without AS Path length", "is_correct": false}]$$::jsonb, $$Local Preference is evaluated before MED. Higher Local Preference wins.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$BGP$$::text, 25.0, '49cf080ce28fba1c', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('f43ade99-14b1-5cff-8f01-4abc54f76d3a', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'analyze', $$OSPF topology:

        [R1]---Area 0---[R2]---Area 1---[R3]
        10.1.1.0/24     10.2.2.0/24

R1 advertises 10.1.1.0/24 into Area 0. What LSA type does R3 see for 10.1.1.0/24?$$::text, $$[{"id": "A", "text": "Type 1", "is_correct": false}, {"id": "B", "text": "Type 2", "is_correct": false}, {"id": "C", "text": "Type 3", "is_correct": true}, {"id": "D", "text": "Type 5", "is_correct": false}]$$::jsonb, $$Inter-area routes are advertised as Type 3 Summary LSAs by ABRs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$OSPF$$::text, 20.0, 'd17bb06963b55eed', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('6e14414d-25ea-5697-9ada-9c6fb90fe87f', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$EVPN-VXLAN campus topology:

   [Leaf1]====[Spine1]====[Leaf2]
   VTEP       VTEP?        VTEP

Which device role is typically NOT a VTEP in a two-tier EVPN-VXLAN campus?$$::text, $$[{"id": "A", "text": "Access/Leaf switch", "is_correct": false}, {"id": "B", "text": "Distribution/Core switch", "is_correct": false}, {"id": "C", "text": "Spine switch", "is_correct": true}, {"id": "D", "text": "WAN edge router", "is_correct": false}]$$::jsonb, $$In a two-tier campus fabric, leaf/access switches act as VTEPs; spine provides IP underlay.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$EVPN/VXLAN$$::text, 20.0, '9d932a184d911c93', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('6eed3a72-f848-5b69-9021-395c4c8c7fb3', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$Multicast topology using PIM-SM:

   [Source]---[R1]---[R2]---[Receiver]
              RP

Which tree is initially built from source to RP?$$::text, $$[{"id": "A", "text": "Shared tree (*,G)", "is_correct": false}, {"id": "B", "text": "Shortest-path tree (S,G)", "is_correct": true}, {"id": "C", "text": "Bidirectional tree", "is_correct": false}, {"id": "D", "text": "None; receivers join directly to source", "is_correct": false}]$$::jsonb, $$In PIM-SM, the source registers with RP and an SPT (S,G) is built from source to RP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$Multicast$$::text, 10.0, '30d5a55ae859e574', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('f8163fbd-9605-539f-b490-81f8a1551daa', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 2, 'understand', $$Refer to the CoS topology:

   [Voice]---[EF Queue]---[Router]---[BE Queue]---[Data]

Which scheduler services EF before BE?$$::text, $$[{"id": "A", "text": "WRR", "is_correct": false}, {"id": "B", "text": "Strict-high priority", "is_correct": true}, {"id": "C", "text": "RED", "is_correct": false}, {"id": "D", "text": "Tail drop", "is_correct": false}]$$::jsonb, $$Strict-high priority queues are serviced before other queues.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$CoS$$::text, 15.0, '3f2a2a7cd4f9a014', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('ae876e47-da97-59ca-bc43-1bf610abb7b9', 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'topology', 3, 'understand', $$Topology:

   [PE1]---[P]---[PE2]
   VPN-A     VPN-A

Which protocol carries VPNv4 routes between PE1 and PE2?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "LDP", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "RSVP", "is_correct": false}]$$::jsonb, $$MP-BGP with VPNv4 address family exchanges customer routes between PEs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"}$$::text[], $$BGP/MPLS$$::text, 10.0, 'f2731ed188698bc3', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a1bd99d1-d88a-522d-bd76-f4ab45c7a1b8', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$MPLS L3VPN topology:

   CE1--PE1--P--PE2--CE2
   VPN-A        VPN-A

Which protocol carries VPNv4 routes between PE1 and PE2?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "LDP", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "RSVP", "is_correct": false}]$$::jsonb, $$MP-BGP with VPNv4 address family exchanges customer routes between PE routers.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$MPLS L3VPN$$::text, 25.0, 'c105f7acabb06dfe', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('9bd1c4ea-dd90-532c-b128-69e467e1a79b', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'analyze', $$RSVP-TE topology:

   [R1]---[R2]---[R3]---[R4]
   All links 10 Gbps except R2-R3 1 Gbps

An LSP from R1 to R4 is signaled with bandwidth 5 Gbps. Which path is chosen by CSPF?$$::text, $$[{"id": "A", "text": "R1-R2-R3-R4", "is_correct": false}, {"id": "B", "text": "R1-R2-R3-R4 if it has lowest IGP metric", "is_correct": false}, {"id": "C", "text": "The path that satisfies 5 Gbps constraint", "is_correct": true}, {"id": "D", "text": "CSPF ignores bandwidth constraints", "is_correct": false}]$$::jsonb, $$CSPF selects a path that meets bandwidth constraints; R2-R3 1 Gbps link cannot carry 5 Gbps LSP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$MPLS TE$$::text, 20.0, 'aec9657203730d2f', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('35d260ad-49bf-575d-9fef-ae5bfaea3687', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$BGP topology with route reflectors:

         [RR]
        /    \
     [PE1]  [PE2]

PE1 receives a VPNv4 route from a CE. How does PE2 learn it?$$::text, $$[{"id": "A", "text": "PE1 sends it directly to PE2", "is_correct": false}, {"id": "B", "text": "PE1 sends it to RR, which reflects to PE2", "is_correct": true}, {"id": "C", "text": "It is flooded via OSPF", "is_correct": false}, {"id": "D", "text": "It is learned via LDP", "is_correct": false}]$$::jsonb, $$Route reflectors eliminate full-mesh iBGP by reflecting routes between clients.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$BGP$$::text, 20.0, '9d8e8a0647f13567', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('480266c0-851d-5388-8703-271724caafa9', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'analyze', $$IS-IS topology:

   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]

All routers are L1/L2. Which statement is true about L1 routes in Area 49.0002?$$::text, $$[{"id": "A", "text": "R3 sees R1's L1 routes natively", "is_correct": false}, {"id": "B", "text": "R2 leaks L1 routes from Area 49.0001 into Area 49.0002 as L2 routes", "is_correct": true}, {"id": "C", "text": "IS-IS does not support route leaking", "is_correct": false}, {"id": "D", "text": "R3 must run L1 only", "is_correct": false}]$$::jsonb, $$L1/L2 routers leak L1 routes into the L2 backbone. By default, L2 routes are not leaked down to L1.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$IS-IS$$::text, 15.0, '4414610a8c82abe4', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('1cdd74a5-f7f2-54ca-8a19-c07e1b897033', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 3, 'understand', $$Segment Routing topology:

   [R1]---[R2]---[R3]
   SRGB 1000-2000 on all nodes

R1 wants to send traffic to R3 using explicit SR path 1002-1003. What does 1003 represent?$$::text, $$[{"id": "A", "text": "R3's prefix SID", "is_correct": true}, {"id": "B", "text": "R2's adjacency SID", "is_correct": false}, {"id": "C", "text": "R1's node SID", "is_correct": false}, {"id": "D", "text": "A service label", "is_correct": false}]$$::jsonb, $$The prefix/node SID for R3 is 1003 within the SRGB.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$Segment Routing$$::text, 20.0, '159e6f01ceb55857', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('08c0ef12-05dc-52ca-a6fa-a072bd2b792f', 'b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002', 'topology', 2, 'understand', $$LDP topology:

   [R1]---[R2]---[R3]

LDP is enabled on all interfaces. Which statement is true?$$::text, $$[{"id": "A", "text": "LDP sessions are TCP-based and established between directly connected neighbors", "is_correct": true}, {"id": "B", "text": "LDP uses UDP only", "is_correct": false}, {"id": "C", "text": "LDP requires RSVP to be enabled", "is_correct": false}, {"id": "D", "text": "LDP labels are advertised only for BGP routes", "is_correct": false}]$$::jsonb, $$LDP discovery uses UDP hello, but session is TCP-based between directly connected neighbors.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"}$$::text[], $$MPLS$$::text, 20.0, 'd72d589396d2f154', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('97e2eb73-443c-56e3-9f5a-8a06ddf1a6ed', 'b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003', 'topology', 2, 'understand', $$Refer to the SRX topology:

   [Untrust]---[SRX Cluster]---[Trust]
                |    |
             Node0 Node1

Which link is used for control-plane communication?$$::text, $$[{"id": "A", "text": "Fabric link", "is_correct": false}, {"id": "B", "text": "Control link", "is_correct": true}, {"id": "C", "text": "Data link", "is_correct": false}, {"id": "D", "text": "HA link", "is_correct": false}]$$::jsonb, $$The control link carries control-plane and state synchronization traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"}$$::text[], $$High Availability$$::text, 20.0, 'e4296deb636ada43', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('930d25b4-9f0e-51f5-ab02-9e982f20e23a', 'b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Topology:

   [User]---[SRX]---[Internet]

SSL Forward Proxy is configured. What can be inspected?$$::text, $$[{"id": "A", "text": "Outbound HTTPS traffic", "is_correct": true}, {"id": "B", "text": "Inbound SSH traffic", "is_correct": false}, {"id": "C", "text": "Outgoing DNS queries only", "is_correct": false}, {"id": "D", "text": "Only unencrypted HTTP", "is_correct": false}]$$::jsonb, $$SSL Forward Proxy decrypts outbound HTTPS traffic for UTM/IPS inspection.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"}$$::text[], $$SSL Proxy$$::text, 20.0, '50e07ed17f269cf3', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('dfa32b67-5abf-521f-99fe-a939a0c0a49f', 'b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Refer to the topology:

   [Zone-A]---[SRX]---[Zone-B]
   10.1.0.0/16      10.2.0.0/16

A security policy allows traffic from Zone-A to Zone-B. What else is required for NAT?$$::text, $$[{"id": "A", "text": "Source NAT rule", "is_correct": true}, {"id": "B", "text": "Destination NAT rule", "is_correct": false}, {"id": "C", "text": "Static NAT rule", "is_correct": false}, {"id": "D", "text": "No NAT needed", "is_correct": false}]$$::jsonb, $$Source NAT is typically required for outgoing traffic from private zones.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"}$$::text[], $$NAT$$::text, 20.0, 'b38ac0fd0cc5ebd3', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('7207f818-1c64-56e1-aa1d-863b5cfc30aa', 'b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Topology:

   [Branch]---IPsec---[HQ]
   10.1.0.0/16      10.2.0.0/16

Which IKE phase establishes the IPsec SA?$$::text, $$[{"id": "A", "text": "IKE Phase 1", "is_correct": false}, {"id": "B", "text": "IKE Phase 2", "is_correct": true}, {"id": "C", "text": "IKE Phase 3", "is_correct": false}, {"id": "D", "text": "Dead Peer Detection", "is_correct": false}]$$::jsonb, $$IKE Phase 2 negotiates the IPsec SA and security parameters.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"}$$::text[], $$VPN$$::text, 20.0, 'a5a9783bd4700bb9', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('38b30cac-ffac-50db-a827-62dfcd4599cb', 'b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003', 'topology', 3, 'understand', $$Refer to the topology:

   [Internet]---[SRX]---[DMZ]---[Web Server]

Which feature protects the Web Server from HTTP floods?$$::text, $$[{"id": "A", "text": "AppDoS", "is_correct": true}, {"id": "B", "text": "Source NAT", "is_correct": false}, {"id": "C", "text": "Route lookup", "is_correct": false}, {"id": "D", "text": "DNS proxy", "is_correct": false}]$$::jsonb, $$AppDoS provides application-layer DoS protection.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"}$$::text[], $$AppSecure$$::text, 20.0, '69a2d72319954a21', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('6612ca6f-5c98-52ee-afc3-1e86af52ceec', 'b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the EVPN-VXLAN topology:

   [Leaf1]====[Spine]====[Leaf2]
   VTEP                  VTEP

Which device typically does NOT run as a VTEP?$$::text, $$[{"id": "A", "text": "Leaf switch", "is_correct": false}, {"id": "B", "text": "Spine switch", "is_correct": true}, {"id": "C", "text": "Border leaf", "is_correct": false}, {"id": "D", "text": "Hypervisor", "is_correct": false}]$$::jsonb, $$Spine switches provide IP underlay only; leaf switches act as VTEPs.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"}$$::text[], $$VXLAN$$::text, 25.0, 'fa3f9101951f2866', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('03fc8fa7-37df-5ed3-9058-2002b41246cc', 'b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [Server1]---[Leaf1]====[Leaf2]---[Server2]
   VNI 10001             VNI 10001

What identifies the shared Layer 2 segment?$$::text, $$[{"id": "A", "text": "VLAN ID", "is_correct": false}, {"id": "B", "text": "VNI", "is_correct": true}, {"id": "C", "text": "Route Distinguisher", "is_correct": false}, {"id": "D", "text": "Loopback IP", "is_correct": false}]$$::jsonb, $$VXLAN Network Identifier (VNI) identifies the Layer 2 overlay segment.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"}$$::text[], $$VXLAN$$::text, 25.0, '1a6738fcc51b1521', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('65db54f5-415e-5758-9058-a341508a9e27', 'b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004', 'topology', 3, 'understand', $$Refer to the topology:

   [Server]---[Leaf1]====[Leaf2]---[Server]
            ES-1         ES-1

What provides active-active multihoming?$$::text, $$[{"id": "A", "text": "MC-LAG", "is_correct": false}, {"id": "B", "text": "EVPN multihoming", "is_correct": true}, {"id": "C", "text": "VRRP", "is_correct": false}, {"id": "D", "text": "LACP", "is_correct": false}]$$::jsonb, $$EVPN multihoming provides active-active L2 multihoming via Ethernet Segments.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"}$$::text[], $$EVPN$$::text, 25.0, '8adf09f8adaef8a7', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('7e83140b-a5bd-5f46-b20b-2e6da655b381', 'b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Topology:

   [Spine1]====[Spine2]
      ||        ||
   [Leaf1]====[Leaf2]

Which protocol carries EVPN routes?$$::text, $$[{"id": "A", "text": "OSPF", "is_correct": false}, {"id": "B", "text": "IS-IS", "is_correct": false}, {"id": "C", "text": "MP-BGP", "is_correct": true}, {"id": "D", "text": "LDP", "is_correct": false}]$$::jsonb, $$EVPN routes are exchanged via MP-BGP.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"}$$::text[], $$EVPN$$::text, 15.0, 'f5f24b69516e17c0', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('234b5519-62e7-50a9-a29a-baea9d1fe810', 'b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004', 'topology', 2, 'understand', $$Refer to the topology:

   [Tenant-A]---[vRouter]---[Underlay]---[vRouter]---[Tenant-B]

Which Contrail component runs on the compute node?$$::text, $$[{"id": "A", "text": "Config node", "is_correct": false}, {"id": "B", "text": "vRouter", "is_correct": true}, {"id": "C", "text": "Control node", "is_correct": false}, {"id": "D", "text": "Analytics node", "is_correct": false}]$$::jsonb, $$Contrail vRouter runs on compute nodes and forwards tenant traffic.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"}$$::text[], $$Contrail$$::text, 15.0, 'b76d20385ed18d09', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('f89bb94e-3c4e-519d-9600-6002242ad75e', 'b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005', 'topology', 1, 'remember', $$Refer to the automation topology:

   [Ansible]---NETCONF---[Junos]

Which module pushes configuration?$$::text, $$[{"id": "A", "text": "ios_config", "is_correct": false}, {"id": "B", "text": "junos_config", "is_correct": true}, {"id": "C", "text": "netconf_rpc", "is_correct": false}, {"id": "D", "text": "template", "is_correct": false}]$$::jsonb, $$junos_config manages Junos configurations via NETCONF.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"}$$::text[], $$Ansible$$::text, 25.0, 'e1f985f6c02ac1cc', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('8133a382-64e1-5507-9687-d3873738254e', 'b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Topology:

   [NETCONF Client]---RPC---[Junos]

Which RPC retrieves the candidate configuration?$$::text, $$[{"id": "A", "text": "<get-config>", "is_correct": true}, {"id": "B", "text": "<edit-config>", "is_correct": false}, {"id": "C", "text": "<copy-config>", "is_correct": false}, {"id": "D", "text": "<delete-config>", "is_correct": false}]$$::jsonb, $$<get-config> retrieves configuration data from a datastore.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"}$$::text[], $$NETCONF$$::text, 25.0, 'de1a92a808a22523', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('a11b1568-6952-5cdd-ac78-d10e0b63c334', 'b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [REST Client]---HTTPS---[Junos REST API]

Which HTTP method partially updates a resource?$$::text, $$[{"id": "A", "text": "POST", "is_correct": false}, {"id": "B", "text": "PUT", "is_correct": false}, {"id": "C", "text": "PATCH", "is_correct": true}, {"id": "D", "text": "GET", "is_correct": false}]$$::jsonb, $$PATCH applies partial updates to a resource.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"}$$::text[], $$REST API$$::text, 25.0, '25ed15520a52caff', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('1b63bd6d-0e8e-5dc3-9ba7-1868c279c11d', 'b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Topology:

   [Git]--->[CI/CD]--->[NETCONF]--->[Junos]

What does this pipeline provide?$$::text, $$[{"id": "A", "text": "Version-controlled automated configuration deployment", "is_correct": true}, {"id": "B", "text": "Faster packet forwarding", "is_correct": false}, {"id": "C", "text": "Physical cabling automation", "is_correct": false}, {"id": "D", "text": "Removes need for routing protocols", "is_correct": false}]$$::jsonb, $$CI/CD with NETCONF enables version-controlled and automated config deployment.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"}$$::text[], $$Automation Concepts$$::text, 25.0, 'b47f9537f66a2507', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ('25499f5d-bc22-5d35-baea-6ec2e2f2fb0b', 'b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005', 'topology', 2, 'understand', $$Refer to the topology:

   [Junos]--->[SYSLOG]--->[Event Script]--->[Action]

Which script type is triggered by syslog events?$$::text, $$[{"id": "A", "text": "Op script", "is_correct": false}, {"id": "B", "text": "Event script", "is_correct": true}, {"id": "C", "text": "Commit script", "is_correct": false}, {"id": "D", "text": "SNMP script", "is_correct": false}]$$::jsonb, $$Event scripts are triggered by syslog events and can take corrective actions.$$::text, $${"https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"}$$::text[], $$Junos Automation$$::text, 25.0, '3d136185112b9016', true) ON CONFLICT (id) DO NOTHING;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DELETE FROM questions WHERE id IN ('ceaf0c7d-b087-553c-a5af-0f7ad61e804e','ac467ceb-1a25-55f0-9c5f-911d6c0ce1ae','187f1f64-9176-5479-ab0c-ee836aa35899','ce4ec3d4-60a2-5bd5-839d-1d4819596455','278ef756-63ba-5a33-8b5d-34b1ec30454b','eb0a1825-2988-5133-b067-77be07bf6c46','2062be02-129b-5ab3-bb16-e737a0e3b71d','37169723-55ca-5dd5-a7a4-a5c0ed9372f1','416fb4f0-7335-5ff1-883d-7f3919462c41','74e45916-5914-54e7-854b-72da1e32daa5','beaa524b-bd93-5c50-884b-07a8a043b4c4','0a6a45bc-5020-5957-a369-c4127041cca4','a56f333d-3637-5a75-915c-5c184ce42c13','2bea8f92-81dc-596b-86d2-4457c70773c4','e96a9e8e-7ddd-5cb3-b5a5-7af3d633da31','6e1fee8a-1a6a-5e71-b5f8-f9aa6a3b47a2','e9a2d356-a127-55e8-bd36-3615067db6f7','a5f163d6-d08d-59a9-bdfa-44ad109efe89','e8d4bd26-8b6a-5967-a793-fc945a0ad808','47f7c09b-4e76-5b7d-b872-e11d1553d7be','a63cbb42-9150-589a-945d-f016b19ef16a','a9509689-36ce-53f7-87a8-7a71fc481627','d6d697e4-1a2f-5573-90ce-2c85aa9f9059','c3c42f9c-4089-5a9b-847f-6bc2adff1c3b','98965450-8653-592a-8a8c-679e2e1398db','0549c95c-885b-501b-9804-76bbc45b360c','acdfab8a-8390-5ade-8d9c-162506daf943','70bbba1e-effe-598a-be55-a5ce0ae6346d','69a1793f-4684-5c51-90a7-ba723c415930','03e18d7d-cc47-5117-b425-a4235a2255a2','beec1ea4-cb8e-5b9d-a4ab-eecc24fd934b','beb3706e-fb52-580d-a319-7196d8f88659','35d48a1e-3970-5808-9626-0cef93a4039d','a5b5bae0-323a-54e7-9a11-80348399940a','b40a6c21-7641-5843-8e10-990fd8d60ab4','45320141-627b-5abb-89af-277cb265baa3','a7481394-441a-5238-84c1-93d4f8db9458','4dde0a19-601a-59fc-b080-8359d34187ce','bd3dc83c-8e97-501f-bfd0-f81f6b5fca92','02f3c731-e82d-5150-96d6-8574ed1d9638','225d24fe-2d9a-54c3-be88-826080bf2357','d238de0a-fe5d-50ae-b5f7-6a4c91d2c18a','4335c6dc-9f33-5bec-882d-ea782cc86d6e','571535f9-c8fa-57e8-8b49-63a2c1fb1766','5613e5fd-3e84-5d4b-99f2-c64a9318b97d','937a1906-ebc0-5751-87ab-137239c26630','66f2efdd-d323-5cfd-9d3c-d7bc6d930951','100e52f7-b53c-5b76-884f-86a20006a3f9','0eca24dc-ef09-5537-99ec-9b296be16ead','e6652dbe-ceab-5fc7-9261-d0f74fb420c0','e5da7d29-544f-5b54-b085-75af7d2136eb','b1f8ecca-ab3b-540a-a79c-3ad15666ea00','9cea0a3f-66d6-5368-93f7-2e53770568a2','667c5ab7-c610-5f55-aba9-d771b0337bba','803f1afe-974f-5cc2-aad1-1d8d8fcfe52f','d0032a6d-1492-5ec6-b0d5-d04895494316','bd905377-4402-5548-b08b-c2ee1d84e355','777b09bd-7b75-597f-9a36-95488b3e68c6','d92c5d5a-dea6-518a-a18b-d62d0a102c61','e62cbe41-77ee-5a70-9455-212613ecbe0c','2b943114-8e52-5946-ba7b-9181bcb3136f','3d3848a8-8454-5f89-8170-81a06af76016','b84c6ba3-fa6f-5268-baef-c3253c6024d4','445b1adf-089f-533c-9d57-621aa9c81a9d','f43ade99-14b1-5cff-8f01-4abc54f76d3a','6e14414d-25ea-5697-9ada-9c6fb90fe87f','6eed3a72-f848-5b69-9021-395c4c8c7fb3','f8163fbd-9605-539f-b490-81f8a1551daa','ae876e47-da97-59ca-bc43-1bf610abb7b9','a1bd99d1-d88a-522d-bd76-f4ab45c7a1b8','9bd1c4ea-dd90-532c-b128-69e467e1a79b','35d260ad-49bf-575d-9fef-ae5bfaea3687','480266c0-851d-5388-8703-271724caafa9','1cdd74a5-f7f2-54ca-8a19-c07e1b897033','08c0ef12-05dc-52ca-a6fa-a072bd2b792f','97e2eb73-443c-56e3-9f5a-8a06ddf1a6ed','930d25b4-9f0e-51f5-ab02-9e982f20e23a','dfa32b67-5abf-521f-99fe-a939a0c0a49f','7207f818-1c64-56e1-aa1d-863b5cfc30aa','38b30cac-ffac-50db-a827-62dfcd4599cb','6612ca6f-5c98-52ee-afc3-1e86af52ceec','03fc8fa7-37df-5ed3-9058-2002b41246cc','65db54f5-415e-5758-9058-a341508a9e27','7e83140b-a5bd-5f46-b20b-2e6da655b381','234b5519-62e7-50a9-a29a-baea9d1fe810','f89bb94e-3c4e-519d-9600-6002242ad75e','8133a382-64e1-5507-9687-d3873738254e','a11b1568-6952-5cdd-ac78-d10e0b63c334','1b63bd6d-0e8e-5dc3-9ba7-1868c279c11d','25499f5d-bc22-5d35-baea-6ec2e2f2fb0b');

-- +goose StatementEnd
