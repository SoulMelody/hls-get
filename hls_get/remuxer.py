import av


def remux(in_name, out_name):
    out_name = f'{out_name}.mp4'
    with open(out_name, 'wb+') as out_file:
        input_ = av.open(in_name, format='hls', options={'codec': 'copy', 'bsf:a': 'aac_adtstoasc'}, metadata_errors='ignore')
        output = av.open(out_file, 'w', format='mp4', metadata_errors='ignore')

        in_to_out = {}

        for stream in input_.streams:
            in_to_out[stream] = output.add_stream(template=stream)

        min_dts = min(stream.start_time or 0 for stream in in_to_out.values())

        for packet in input_.demux(tuple(in_to_out.keys())):
            if packet.dts is not None:
                packet.dts -= min_dts
                packet.stream = in_to_out[packet.stream]
                output.mux(packet)

        output.close()
