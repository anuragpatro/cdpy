# -*- coding: utf-8 -*-

# from cdpy.common import CdpSdkBase, Squelch
from .common import CdpSdkBase, Squelch


class CdpyDe(CdpSdkBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_services(self, remove_deleted: bool = False, env: str = None):
        result = self.sdk.call(svc='de', func='list_services', ret_field='services', removeDeleted=remove_deleted)
        if env:
            return [x for x in result if x['environmentName'] == env]
        return result

    def list_vcs(self, cluster_id):
        return self.sdk.call(
            svc='de', func='list_vcs', ret_field='vcs', squelch=[
                Squelch(value='NOT_FOUND', default=list())
            ],
            clusterId=cluster_id
        )

    def describe_service(self, cluster_id: str):
        return self.sdk.call(
            svc='de', func='describe_service', ret_field='service', squelch=[
                Squelch(value='NOT_FOUND'), Squelch('INVALID_ARGUMENT')
            ],
            clusterId=cluster_id
        )

    def describe_vc(self, cluster_id, vc_id):
        return self.sdk.call(
            svc='de', func='describe_vc', ret_field='vc', squelch=[
                Squelch(value='NOT_FOUND'), Squelch('INVALID_ARGUMENT')
            ],
            clusterId=cluster_id, vcId=vc_id
        )

    def enable_service(self, name: str, env_crn: str, instance_type: str, minimum_instances: int = None,
                       maximum_instances: int = None, minimum_spot_instances: int = None,
                       maximum_spot_instances: int = None, initial_instances: int = None,
                       initial_spot_instances: int = None, root_volume_size: int = None,
                       public_load_balancer: bool = False, enable_workload_analytics: bool = False,
                       use_ssd: bool = False, chart_value_overrides: dict = None, authorized_ips: list = None,
                       tags: dict = None, validation_check: bool = False):
        # self.sdk.validate_crn(env_crn)

        if chart_value_overrides is not None:
            chart_overrides = []
            for chartName, overrides in chart_value_overrides.items():
                chart_overrides.append({'chartName': chartName, 'overrides': overrides})
        else:
            chart_overrides = None

        return self.sdk.call(
            svc='de', func='enable_service', ret_field='service', name=name, env=env_crn, instanceType=instance_type,
            minimumInstances=minimum_instances, maximumInstances=maximum_instances,
            minimumSpotInstances=minimum_spot_instances, maximumSpotInstances=maximum_spot_instances,
            initialInstances=initial_instances, initialSpotInstances=initial_spot_instances,
            rootVolumeSize=root_volume_size, enablePublicEndpoint=public_load_balancer,
            enableWorkloadAnalytics=enable_workload_analytics, useSsd=use_ssd, chartValueOverrides=chart_overrides,
            whitelistIps=authorized_ips, tags=tags, skipValidation=validation_check, squelch=[
                Squelch(field='error_code', value='CONFLICT', default=list(),
                        warning="CDE Service with name %s already exists." % name)
            ]
        )

    def disable_service(self, cluster_id: str, force: bool = False):
        return self.sdk.call(
            svc='de', func='disable_service', squelch=[
                Squelch(value='NOT_FOUND'),
                Squelch(field='error_code', value='UNKNOWN', default=list(),
                        warning="Invalid Cluster State for Disabling Service.")
            ],
            clusterId=cluster_id, force=force
        )

    def create_vc(self, name: str, cluster_id: str, cpu_requests: str, memory_requests: str,
                  runtime_spot_component: str, chart_value_overrides: dict = None):

        if chart_value_overrides is not None:
            chart_overrides = []
            for chartName, overrides in chart_value_overrides.items():
                chart_overrides.append({'chartName': chartName, 'overrides': overrides})
        else:
            chart_overrides = None

        return self.sdk.call(
            svc='de', func='create_vc', ret_field='Vc', name=name, clusterId=cluster_id, cpuRequests=cpu_requests,
            memoryRequests=memory_requests, chartValueOverrides=chart_overrides,
            runtimeSpotComponent=runtime_spot_component, squelch=[
                Squelch(field='error_code', value='CONFLICT', default=list(),
                        warning="Virtual Cluster with name %s already exists." % name)
            ]
        )

    def delete_vc(self, cluster_id: str, vc_id: str):
        return self.sdk.call(
            svc='de', func='delete_vc', squelch=[
                Squelch(value='NOT_FOUND'),
                Squelch(field='error_code', value='UNKNOWN', default=list(),
                        warning="Invalid App Instance State for Deletion.")
            ],
            clusterId=cluster_id, vcId=vc_id
        )
