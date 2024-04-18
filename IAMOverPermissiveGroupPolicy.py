import connection.GenerateFindings as GenerateFindings

def get_over_permissive_group_policy(group_details):
    group_list = []
    
    for group in group_details:
        over_permissive_policies = set()
        group_info = {"Group Name": group['GroupName'], "Policies": ""}
        for policy in group['GroupPolicy']:
            policy_document = policy['PolicyDocument']
            statements = policy_document['Statement']
            if isinstance(statements, dict):
                statements = [statements]
            for statement in statements:
                if "Action" in statement:
                    if isinstance(statement['Action'], str):
                        actions = [statement['Action']]
                    if isinstance(statement['Action'], list):
                        actions = statement['Action']
                    if actions is not None:
                        for action in actions:
                            if (
                                action == "*" and statement.get('Effect') == "Allow" or 
                                action == "iam:*" and statement.get('Effect') == "Allow" or
                                (action == "iam:PassRole" and statement.get('Resource') == "*") or
                                (statement.get('NotAction') and statement.get('Effect') == "Allow")
                            ):
                                over_permissive_policies.add(policy['PolicyName'])
                                break
        if over_permissive_policies:
            group_info["Policies"] = ", ".join(over_permissive_policies)
            group_list.append(group_info)    
    return group_list


def lambda_handler(request_data, group_details):
    id = 118

    resource = GenerateFindings.get_finding_data(id, request_data)

    if resource is None:
        resource = dict()
        response = get_over_permissive_group_policy(group_details)
        resource["id"] = id
        resource["severity"] = "HIGH"
        resource["name"] = "IAM - Overly Permissive IAM Group Policies"
        resource["compliance"] = "Cloudscraper"
        resource['reference_link'] = "https://www.trendmicro.com/cloudoneconformity-staging/knowledge-base/aws/IAM/iam-group-policy-too-permissive.html"
        resource["description"] = "Ensure that Amazon IAM policies attached to IAM Group policies aren't too permissive."
        resource["fields"] = {"1": "Group Name", "2" : "Policies"}
        resource["count"] = len(response)
        resource["resource"] = response

        GenerateFindings.put_finding_data(id, request_data, resource)

    return resource
