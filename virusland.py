import sys
import vutils
import vassemble
import vmap
import vparse
# pass list of arguments to VSetup
vconf = vutils.VSetup(sys.argv[1:])
#vconf.check_dependencies() TODO fix dependency checkers

vasm = vassemble.VAssemble(
                            vconf.args.finput,
                            vconf.args.paired_end_reads,
                            vconf.args.threads
                          )

if vconf.args.quality_control is True:
    vasm.run_qc(vconf.out_dirs['trimmed'])

if vconf.args.assembled_contigs is False:
    vasm.run_assembly(vconf.args.assembler, vconf.out_dirs['assembled'])
    contigs = vasm.contigs
else:
    contigs = vconf.args.finput[0] # TODO make nicer
print('contigs:', contigs )
vparser = vparse.VParse()
vparser.parse_index(vconf.args.index, vconf.out_dirs['mapped'])
# TODO clean up these functins, everything shouldnt be in constructor if possible 
vmapper = vmap.VMap(contigs, 
                    vconf.args.mapper, 
                    vconf.out_dirs['mapped'], 
                    vconf.args.threads)
vmapper.build_index(vparser.index_file)
vmapper.run_map()

vparser.parse_hits_file(vmapper.hit_file, 50) # TODO make bitscore arg w default 50
vparser.generate_statistics()
vparser.write_out_all_stats(vconf.out_dirs['stats'])