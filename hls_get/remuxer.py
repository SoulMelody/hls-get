import av


def remux(in_name, out_name):
    out_name = f'{out_name}.mp4'
    with open(out_name, 'wb+') as out_file:
        input_ = av.open(in_name, format='hls', options={
            'vcodec': 'copy',
            'acodec': 'aac',
            'bsf:a': 'aac_adtstoasc'
        }, metadata_errors='ignore')
        output = av.open(out_file, 'w', format='mp4', options={
            'strict': '-1'
        }, metadata_errors='ignore')

        in_to_out = {
            stream: output.add_stream(template=stream)
            for stream in input_.streams
        }

        for packet in input_.demux(tuple(input_.streams)):
            try:
                if packet.dts is not None:
                    packet.stream = in_to_out[packet.stream]
                    output.mux(packet)
            except av.AVError:
                pass

        output.close()
        return out_file.tell()
